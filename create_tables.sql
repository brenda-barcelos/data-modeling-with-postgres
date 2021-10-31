rollback;
begin;

drop table if exists dim_user;
drop table if exists dim_song;
drop table if exists dim_artist;
drop table if exists dim_time;
drop table if exists fac_songplay;

/* user in the app */
create table dim_user (
    user_id int, 
    first_name varchar, 
    last_name varchar, 
    gender varchar, 
    level varchar,
    constraint pk_dim_user primary key (user_id)
);

/* song in music db */
create table dim_song( 
    song_id varchar, 
    title varchar, 
    artist_id varchar,
    year int, 
    duration numeric,
    constraint pk_dim_song primary key (song_id)
);

/* artist in music db */
create table dim_artist( 
    artist_id varchar, 
    name varchar, 
    location varchar, 
    latitude numeric, 
    longitude numeric,
    constraint pk_dim_artist primary key (artist_id)
);

/* timestamps ofrecords in songplay broken down into specific units */
create table dim_time( 
    start_time timestamp,
    hour int, 
    day int, 
    week int, 
    month int, 
    year int,
    weekday int, -- 1 a 7
    constraint pk_dim_times primary key (start_time)
);


/* records in log data associated with song plays i.e. records */
create table fac_songplay ( 
    songplay_id serial,
    start_time timestamp, 
    user_id int, 
    level varchar, 
    song_id int, 
    artist_id varchar, 
    session_id int, 
    location varchar, 
    user_agent varchar
    --, constraint primary key pk_fac_songplay on (songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location)

