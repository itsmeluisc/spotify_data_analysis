-- sql/01_create_staging_table.sql
-- Brief Description: Drops the existing staging table (if present) and then creates a new
-- spotify_songs_staging table with all columns initially defined as TEXT to facilitate
-- raw data ingestion.

/*---------------------------------------------------------------------------------------------------
---------------------------------DROP AND CREATE STAGING TABLE---------------------------------------
---------------------------------------------------------------------------------------------------*/

DROP TABLE IF EXISTS spotify_songs_staging;

CREATE TABLE spotify_songs_staging (
    id                   SERIAL PRIMARY KEY,
    spotify_id           TEXT,
    name                 TEXT,
    artists              TEXT,
    daily_rank           TEXT,
    daily_movement       TEXT,
    weekly_movement      TEXT,
    country              TEXT,
    snapshot_date        TEXT,
    popularity           TEXT,
    is_explicit          TEXT,
    duration_ms          TEXT,
    album_name           TEXT,
    album_release_date   TEXT,
    danceability         TEXT,
    energy               TEXT,
    key                  TEXT,
    loudness             TEXT,
    mode                 TEXT,
    speechiness          TEXT,
    acousticness         TEXT,
    instrumentalness     TEXT,
    liveness             TEXT,
    valence              TEXT,
    tempo                TEXT,
    time_signature       TEXT
);