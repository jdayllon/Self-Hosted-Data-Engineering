import os
import glob
import psycopg2
import pandas as pd
import numpy as np
from sql_queries import *
from datetime import datetime

def get_files(filepath):
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))
    
    return all_files

def song_table_insert(cur, data):
    # Insert row
    try: 
        cur.execute(insert_songs, list(data.values))
        cur.connection.commit()
        return True
    except psycopg2.Error as e:
        print("Error: Could not create a row")
        print(e)
        cur.connection.rollback()
        
        return False

def artist_table_insert(cur, data):
    # Insert row
    try: 
        cur.execute(insert_artist, list(data.values))
        cur.connection.commit()
        return True
    except psycopg2.Error as e:
        print(f"Error: Could not create a row: {data.values}")
        print(e)
        cur.connection.rollback()
        
        return False

def time_table_insert(cur, data):
    # Insert row
    try: 
        cur.execute(insert_time, list(data.values))
        cur.connection.commit()
        return True
    except psycopg2.Error as e:
        print("Error: Could not create a row")
        print(e)
        cur.connection.rollback()
        
        return False
    
def user_table_insert(cur, data):
    # Insert row
    try: 
        cur.execute(insert_users, list(data.values))
        cur.connection.commit()
        return True
    except psycopg2.Error as e:
        print(f"Error: Could not create a row: {data.values}")
        print(e)
        cur.connection.rollback()
        
        return False

def songplay_table_insert(cur, data):
    # Insert row
    try: 
        cur.execute(
        """
        INSERT INTO songplays (start_time, user_id, level, song_id, artist_id,session_id,location,user_agent) \
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, list(data.values))
        cur.connection.commit()
        return True
    except psycopg2.Error as e:
        print(f"Error: Could not create a row: {data.values}")
        print(e)
        cur.connection.rollback()
        
        return False        

def song_select(cur, title, artist_name, duration):
    # Search for a song id
    try: 
        cur.execute(
        """
        SELECT songs.song_id, songs.artist_id
        FROM songs
        JOIN artists on songs.artist_id = artists.artist_id
        WHERE songs.title = %s
        AND artists.name = %s
        AND songs.duration = %s
        """, (title, artist_name, duration))

        res = cur.fetchone()
        if res is None:
            return pd.Series([None,None])
        else:
            return pd.Series(res)
    except psycopg2.Error as e:
        print(f"Error: Could not read a row")
        print(e)
        cur.connection.rollback()
        
        return pd.Series([None,None])



def process_song_file(cur, filepath):
    """
        This function reads JSON files and read information of song and artist data and saves into song_data and artist_data
        Arguments:
        cur: Database Cursor
        filepath: location of JSON files
        Return: None
    """
    song_files = [cf for cf in get_files('data/song_data/') if "ipynb" not in cf]
    df_song_file = []

    for cf in song_files:
        df_song_file += [pd.read_json(cf,lines=True)]

    df_song_file = pd.concat(df_song_file).reset_index().drop('index',1)
    df_song_data = df_song_file[['song_id','title','artist_id','year','duration']]
    
    df_song_data.apply(lambda d: song_table_insert(cur,d),1)
    
    df_artist_data = df_song_file[['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']]
    df_artist_data.apply(lambda d: artist_table_insert(cur,d),1)

    return df_song_file


def process_log_file(cur, filepath):
    """
        This function reads Log files and reads information of time, user and songplay data and saves into time, user, songplay
        Arguments:
        cur: Database Cursor
        filepath: location of Log files
        Return: None
    """

    log_files = [cf for cf in get_files('data/log_data/') if "ipynb" not in cf]

    df_log_file = []

    for cf in log_files:
        df_log_file += [pd.read_json(cf,lines=True)]

    df_log_file = pd.concat(df_log_file).reset_index().drop('index',1).query("page == 'NextSong'")
    df_log_file.head()

    df_log_file['ts_date'] = df_log_file['ts'].apply(lambda x: datetime.fromtimestamp(x / 1000))

    column_labels = list(('start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday'))

    time_df = pd.DataFrame(
        df_log_file['ts_date'].apply(lambda x: (x, x.hour, x.day, x.week, x.month, x.year, x.weekday())).tolist(),
        columns = column_labels
    )
    
    time_df.apply(lambda d: time_table_insert(cur,d),1)
    
    user_df = df_log_file[['userId','firstName','lastName','gender','level']]
    user_df = user_df.drop(user_df.query('userId == ""').index)
    user_df['userId'] = user_df['userId'].apply(lambda x: int(x))
    user_df = user_df.sort_values(by=['userId']).drop_duplicates()
    
    user_df.apply(lambda d: user_table_insert(cur,d),1)

    return df_log_file


def process_data(cur, conn, filepath, func):
    
    return func(cur, filepath)

def main():
    conn = psycopg2.connect("host=127.0.0.1 port=30432 dbname=sparkifydb user=sparkify password=sparkify")
    cur = conn.cursor()
    
    # Prepare Database
    try:             
 
        # Droping tables
        for cur_table in drop_table_queries:    
            cur.execute(cur_table)
            cur.connection.commit()
            
        # Creating tables
        for cur_table in create_table_queries:    
            cur.execute(cur_table)
            cur.connection.commit()

        process_data(cur, conn, filepath='data/song_data', func=process_song_file)
        df_log_file = process_data(cur, conn, filepath='data/log_data', func=process_log_file)

        # Populate SongPlays

        df_song_info = pd.DataFrame(df_log_file[['song','artist','length']].apply(lambda x: song_select(cur, x['song'],x['artist'],x['length']),1))
        df_song_info.columns = ['song_id','artist_id']

        songsplay_df = df_log_file[['ts_date','userId','level','sessionId','location','userAgent']].merge(df_song_info,left_index=True, right_index=True)
        songsplay_df = songsplay_df[['ts_date','userId','level','song_id','artist_id','sessionId','location','userAgent']]

        songsplay_df.apply(lambda d: songplay_table_insert(cur,d),1)

    except psycopg2.Error as e:
        print("Error: Could not create a table")
        print(e)

    conn.close()


if __name__ == "__main__":
    main()