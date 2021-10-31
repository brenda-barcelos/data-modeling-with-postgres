# DROP TABLES

songplay_table_drop = "drop table if exists fac_songplay;"
user_table_drop = "drop table if exists dim_user;"
song_table_drop = "drop table if exists dim_song;"
artist_table_drop = "drop table if exists dim_artist;"
time_table_drop = "drop table if exists dim_time;"

# CREATE TABLES

songplay_table_create = ("""
create table fac_songplay ( 
    songplay_id serial, 
    start_time timestamp,
    user_id int, 
    level varchar, 
    song_id varchar, 
    artist_id varchar, 
    session_id int, 
    location varchar, 
    user_agent varchar, 
    constraint pk_fac_songplay primary key (songplay_id)
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
    song_id varchar, 
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
    start_time timestamp,
    hour int, 
    day int, 
    week int, 
    month int, 
    year int,
    weekday int, -- 1 a 7
    constraint pk_dim_time primary key (start_time)
);
""")

# INSERT RECORDS

songplay_table_insert = (""" insert into fac_songplay (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
                             values ( %s, %s, %s, %s, %s, %s, %s, %s)
                             on conflict on constraint pk_fac_songplay do nothing;
""")

user_table_insert = (""" insert into dim_user (user_id, first_name, last_name, gender, level)
                             values (%s, %s, %s, %s, %s)
                             on conflict on constraint pk_dim_user do nothing;
""")

song_table_insert = (""" insert into dim_song (song_id, title, artist_id, year, duration)
                             values (%s, %s, %s, %s, %s)
                             on conflict on constraint pk_dim_song do nothing;
""")

artist_table_insert = (""" insert into dim_artist (artist_id, name, location, latitude, longitude)
                             values (%s, %s, %s, %s, %s)
                             on conflict on constraint pk_dim_artist do nothing;
""")


time_table_insert = (""" insert into dim_time (start_time, hour, day, week, month, year, weekday)
                             values (%s, %s, %s, %s, %s, %s, %s)
                             on conflict on constraint pk_dim_time do nothing;
""")

# FIND SONGS

song_select = ("""  select song_id, artist_id 
                    from dim_song
                    join dim_artist using (artist_id)
                    where title = %s 
                      and name = %s
                      and duration = %s;
""")

# FOREIGN KEYS
fk_artist_songplay = ("""
alter table fac_songplay add constraint fk_artist_songplay_01 foreign key(artist_id)
references dim_artist (artist_id) match simple on update cascade;
""")

fk_song_songplay = ("""
alter table fac_songplay add constraint fk_song_songplay_01 foreign key(song_id)
references dim_song (song_id) match simple on update cascade;
""")

fk_user_songplay = ("""
alter table fac_songplay add constraint fk_user_songplay_01 foreign key(user_id)
references dim_user (user_id) match simple on update cascade;
""")

fk_time_songplay = ("""
alter table fac_songplay add constraint fk_time_songplay_01 foreign key(start_time)
references dim_time (start_time) match simple on update cascade;
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
foreign_keys_queries = [fk_artist_songplay, fk_song_songplay, fk_time_songplay, fk_user_songplay]