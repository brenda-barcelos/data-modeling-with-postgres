# DROP TABLES

songplay_table_drop = "drop table if exists dw.fac_songplay;"
user_table_drop = "drop table if exists dw.dim_user;"
song_table_drop = "drop table if exists dw.dim_song;"
artist_table_drop = "drop table if exists dw.dim_artist;"
time_table_drop = "drop table if exists dw.dim_time;"

# CREATE TABLES

songplay_table_create = ("""
create table dw.fac_songplay ( 
    songplay_id     serial      not null, 
    start_time      timestamp   not null,
    user_id         int         not null, 
    level           varchar     not null, 
    song_id         varchar         null, 
    artist_id       varchar         null, 
    session_id      int         not null, 
    location        varchar     not null, 
    user_agent      varchar     not null, 
    constraint pk_fac_songplay primary key (songplay_id)
);
""")

user_table_create = ("""
create table dw.dim_user (
    user_id     int     not null, 
    first_name  varchar not null, 
    last_name   varchar not null, 
    gender      varchar not null, 
    level       varchar not null,
    constraint pk_dim_user primary key (user_id)
);
""")

song_table_create = ("""
create table dw.dim_song( 
    song_id     varchar     not null, 
    title       varchar     not null, 
    artist_id   varchar     not null,
    year        int         not null, 
    duration    numeric     not null,
    constraint pk_dim_song primary key (song_id)
);
""")

artist_table_create = ("""
create table dw.dim_artist( 
    artist_id   varchar     not null, 
    name        varchar     not null, 
    location    varchar         null, 
    latitude    numeric         null, 
    longitude   numeric         null,
    constraint pk_dim_artist primary key (artist_id)
);
""")

time_table_create = ("""
create table dw.dim_time( 
    start_time timestamp    not null,
    hour int                not null, 
    day int                 not null, 
    week int                not null, 
    month int               not null, 
    year int                not null,
    weekday int             not null, /* 0 - 7 */
    constraint pk_dim_time primary key (start_time)
);
""")

# INSERT RECORDS

songplay_table_insert = (""" insert into dw.fac_songplay (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
                             values ( %s, %s, %s, %s, %s, %s, %s, %s)
                             on conflict on constraint pk_fac_songplay do nothing;
""")

user_table_insert = (""" insert into dw.dim_user (user_id, first_name, last_name, gender, level)
                             values (%s, %s, %s, %s, %s)
                             on conflict on constraint pk_dim_user do update
                             set (first_name, last_name, gender, level) = (excluded.first_name, excluded.last_name, excluded.gender, excluded.level)
                             ;
""")

song_table_insert = (""" insert into dw.dim_song (song_id, title, artist_id, year, duration)
                             values (%s, %s, %s, %s, %s)
                             on conflict on constraint pk_dim_song do update
                             set (title, artist_id, year, duration) = (excluded.title, excluded.artist_id, excluded.year, excluded.duration)
                             ;
""")

artist_table_insert = (""" insert into dw.dim_artist (artist_id, name, location, latitude, longitude)
                             values (%s, %s, %s, %s, %s)
                             on conflict on constraint pk_dim_artist do update
                             set (name, location, latitude, longitude) = (excluded.name, excluded.location, excluded.latitude, excluded.longitude)
                             ;
""")


time_table_insert = (""" insert into dw.dim_time (start_time, hour, day, week, month, year, weekday)
                             values (%s, %s, %s, %s, %s, %s, %s)
                             on conflict on constraint pk_dim_time do nothing;
""")

# FIND SONGS

song_select = ("""  select song_id, artist_id 
                    from dw.dim_song
                    join dw.dim_artist using (artist_id)
                    where title = %s 
                      and name = %s
                      and duration = %s;
""")

# FOREIGN KEYS
fk_artist_songplay = ("""
alter table dw.fac_songplay add constraint fk_artist_songplay_01 foreign key(artist_id)
references dw.dim_artist (artist_id) match simple on update cascade;
""")

fk_song_songplay = ("""
alter table dw.fac_songplay add constraint fk_song_songplay_01 foreign key(song_id)
references dw.dim_song (song_id) match simple on update cascade;
""")

fk_user_songplay = ("""
alter table dw.fac_songplay add constraint fk_user_songplay_01 foreign key(user_id)
references dw.dim_user (user_id) match simple on update cascade;
""")

fk_time_songplay = ("""
alter table dw.fac_songplay add constraint fk_time_songplay_01 foreign key(start_time)
references dw.dim_time (start_time) match simple on update cascade;
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
foreign_keys_queries = [fk_artist_songplay, fk_song_songplay, fk_time_songplay, fk_user_songplay]
