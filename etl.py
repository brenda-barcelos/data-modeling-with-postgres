import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Process json song files and insert songs and artist data into Sparkify DB.

    Arguments:
        cur: psycopg2 cursor
        filepath: directory of the song json files
    
    Output:
        None
    """
    # open song file
    df = pd.read_json(filepath, lines = True)

    # insert song record
    song_data = df[['song_id','title','artist_id','year','duration']].values.tolist()[0]
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']].values.tolist()[0]
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Process json log files and insert time, songplays and users data into Sparkify DB.

    Arguments:
        cur: psycopg2 cursor
        filepath: directory of the log json files
    
    Output:
        None
    """
    
    # open log file
    df = pd.read_json(filepath, lines = True)

    # filter by NextSong action
    df = df[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    df['ts'] = pd.to_datetime(df['ts'], unit = 'ms')
    
    
    # insert time data records
    time_data = list([df['ts'], df['ts'].dt.hour, df['ts'].dt.day, df['ts'].dt.isocalendar().week, df['ts'].dt.month, df['ts'].dt.year, df['ts'].dt.weekday])
    column_labels = (['start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday'])
    time_df = dict(zip(column_labels,time_data))
    time_df = pd.DataFrame(time_df)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))
    


    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']]
    user_df = user_df.drop_duplicates()

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row['ts'], row['userId'], row['level'], songid, artistid, row['sessionId'], row['location'], row['userAgent'])
        cur.execute(songplay_table_insert, songplay_data)



def process_data(cur, conn, filepath, func, func_fk):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        #conn.commit()
        print('{}/{} files processed.'.format(i, num_files))

    #print(func_fk is None)
    if func_fk is not None:
        func_fk(cur)

    conn.commit()

def create_fks(cur):

    # creating fks after inserting the data
    cur.execute(fk_user_songplay)
    cur.execute(fk_artist_songplay)
    cur.execute(fk_song_songplay)
    cur.execute(fk_time_songplay)

def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file, func_fk=None)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file, func_fk=create_fks)
    conn.close()


if __name__ == "__main__":
    main()