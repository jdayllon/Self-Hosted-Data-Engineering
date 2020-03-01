import os
import glob
import psycopg2
import pandas as pd
import numpy as np
from sql_queries import *


def process_song_file(cur, filepath):
    """
        This function reads JSON files and read information of song and artist data and saves into song_data and artist_data
        Arguments:
        cur: Database Cursor
        filepath: location of JSON files
        Return: None
    """
    pass


def process_log_file(cur, filepath):
    """
        This function reads Log files and reads information of time, user and songplay data and saves into time, user, songplay
        Arguments:
        cur: Database Cursor
        filepath: location of Log files
        Return: None
    """

   pass


def process_data(cur, conn, filepath, func):

    pass


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()