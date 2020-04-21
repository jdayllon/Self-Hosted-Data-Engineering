# DROP TABLES

drop_table_songplays = "DROP TABLE IF EXISTS songplays"
drop_table_songs = "DROP TABLE IF EXISTS songs"
drop_table_artist =  "DROP TABLE IF EXISTS artists"
drop_table_time = "DROP TABLE IF EXISTS time"
drop_table_users = "DROP TABLE IF EXISTS users"

# CREATE TABLES

create_table_users = """
CREATE TABLE IF NOT EXISTS users
(
    user_id SMALLINT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    gender VARCHAR(1),
    level VARCHAR(4)
)"""

create_table_songs = """
CREATE TABLE IF NOT EXISTS songs
(
    song_id VARCHAR(18) PRIMARY KEY,
    title TEXT,
    artist_id VARCHAR(18),
    year SMALLINT,
    duration NUMERIC
)"""

create_table_artist = """
CREATE TABLE IF NOT EXISTS artists
(
    artist_id VARCHAR(18) PRIMARY KEY,
    name TEXT,
    location TEXT,
    latitude NUMERIC,
    longitude NUMERIC
)"""

create_table_time = """
CREATE TABLE IF NOT EXISTS time
(
    start_time TIMESTAMP PRIMARY KEY,
    hour SMALLINT,
    day SMALLINT,
    week SMALLINT,
    month SMALLINT,
    year SMALLINT,
    weekday SMALLINT
)"""

create_table_songplays = """
CREATE TABLE IF NOT EXISTS songplays
(
    songplay_id SERIAL PRIMARY KEY,
    start_time TIMESTAMP REFERENCES time(start_time),
    user_id SMALLINT REFERENCES users(user_id),
    level VARCHAR(4),
    song_id VARCHAR(18),
    artist_id VARCHAR(18),
    session_id SMALLINT,
    location TEXT,
    user_agent TEXT
)"""

# INSERT RECORDS

## https://www.postgresql.org/docs/9.5/sql-insert.html

insert_songs = """
INSERT INTO songs (song_id, title, artist_id, year, duration) \
VALUES (%s,%s,%s,%s,%s)
"""
insert_artist = """
INSERT INTO artists (artist_id, name, location, latitude, longitude) \
VALUES (%s,%s,%s,%s,%s)
"""

insert_time = """
INSERT INTO time (start_time, hour, day, week, month, year, weekday) \
VALUES (%s,%s,%s,%s,%s,%s,%s)
"""

insert_users = """
INSERT INTO users (user_id, first_name, last_name, gender, level) \
VALUES (%s,%s,%s,%s,%s)
"""
insert_songplays = """
INSERT INTO songplays (start_time, user_id, level, song_id, artist_id,session_id,location,user_agent) \
VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
"""

# FIND SONGS

query_songs = """
SELECT songs.song_id, songs.artist_id
FROM songs
JOIN artists on songs.artist_id = artists.artist_id
WHERE songs.title = %s
AND artists.name = %s
AND songs.duration = %s
"""

# QUERY LISTS
create_table_queries = [create_table_users, create_table_songs, create_table_artist, create_table_time, create_table_songplays]
drop_table_queries = [drop_table_users, drop_table_time, drop_table_artist, drop_table_songs, drop_table_songplays]