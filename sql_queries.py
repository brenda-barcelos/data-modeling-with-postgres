# DROP TABLES

songplay_table_drop = "drop table if exists fac_songplay;"
user_table_drop = "drop table if exists dim_user;"
song_table_drop = "drop table if exists dim_song;"
artist_table_drop = "drop table if exists dim_artist;"
time_table_drop = "drop table if exists dim_time;"

# CREATE TABLES

songplay_table_create = ("""
create table fac_songplay ( 
    songplay_id int, 
    start_time int, 
    user_id int, 
    level varchar, 
    song_id int, 
    artist_id varchar, 
    session_id int, 
    location varchar, 
    user_agent varchar
    --, constraint primary key pk_fac_songplay on (songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location)
);
""")

user_table_create = ("""
create table dim_user (
    user_id int, 
    first_name varchar, 
    last_name varchar, 
    gender varchar, 
    level varchar,
    constraint pk_dim_user primary key (user_id)
);
""")

song_table_create = ("""
create table dim_song( 
    song_id int, 
    title varchar, 
    artist_id varchar,
    year int, 
    duration numeric,
    constraint pk_dim_song primary key (song_id)
);
""")

artist_table_create = ("""
create table dim_artist( 
    artist_id varchar, 
    name varchar, 
    location varchar, 
    latitude numeric, 
    longitude numeric,
    constraint pk_dim_artist primary key (artist_id)
);
""")

time_table_create = ("""
create table dim_time( 
    start_time int, 
    hour int, 
    day int, 
    week int, 
    month int, 
    year int,
    weekday int, -- 1 a 7
    constraint pk_dim_times primary key (start_time)
);
""")

# INSERT RECORDS

songplay_table_insert = (""" insert into fac_songplay (songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
                             values (%s, %s, %s, %s, %s, %s, %s, %s, %s);
""")

user_table_insert = (""" insert into dim_user (user_id, first_name, last_name, gender, level)
                             values (%s, %s, %s, %s, %s);
""")

song_table_insert = (""" insert into dim_song (song_it, title, artist_id, year, duration)
                             values (%s, %s, %s, %s, %s);
""")

artist_table_insert = (""" insert into (artist_id, name, location, latitude, longitude)
                             values (%s, %s, %s, %s, %s);
""")


time_table_insert = (""" insert into (start_time, hour, day, week, month, year, weekday)
                             values (%s, %s, %s, %s, %s, %s, %s);
""")

# FIND SONGS

song_select = (""" select * from dim_song where song_title = %s ;
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
