-- sql/02_ingest_raw_data.sql
-- Brief Description: Copies raw data from the specified CSV file into the spotify_songs_staging table.

/*---------------------------------------------------------------------------------------------------
---------------------------------COPY CSV INTO STAGING TABLE-----------------------------------------
---------------------------------------------------------------------------------------------------*/

COPY spotify_songs_staging (
    spotify_id,
    name,
    artists,
    daily_rank,
    daily_movement,
    weekly_movement,
    country,
    snapshot_date,
    popularity,
    is_explicit,
    duration_ms,
    album_name,
    album_release_date,
    danceability,
    energy,
    key,
    loudness,
    mode,
    speechiness,
    acousticness,
    instrumentalness,
    liveness,
    valence,
    tempo,
    time_signature
)
FROM 'C:\data_analysis\sql\universal_top_spotify_songs.csv'
WITH (
    FORMAT csv,
    HEADER true,
    DELIMITER ',',
    NULL ''
);