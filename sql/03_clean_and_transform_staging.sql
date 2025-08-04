-- sql/03_clean_and_transform_staging.sql
-- Brief Description: This script performs a series of cleaning and transformation operations on the
-- spotify_songs_staging table. This includes handling NULLs, casting to appropriate data types,
-- standardizing song metadata, and managing country codes.

/*---------------------------------------------------------------------------------------------------
---------------------------UPDATE TABLE  -> CONVERT EMPTY STRING "" TO NULL--------------------------
---------------------------------------------------------------------------------------------------*/

UPDATE spotify_songs_staging
SET
    album_release_date = NULLIF(TRIM(album_release_date), ''),
    country              = NULLIF(TRIM(country), ''),
    album_name          = NULLIF(TRIM(album_name), ''),
    name                = NULLIF(TRIM(name), ''),
    artists             = NULLIF(TRIM(artists), '');

/*---------------------------------------------------------------------------------------------------
--------------------------ALTER TABLE -> CAST TO MOST EFFICIENT DATA TYPE----------------------------
---------------------------------------------------------------------------------------------------*/

ALTER TABLE spotify_songs_staging
    ALTER COLUMN spotify_id TYPE CHAR(22) USING spotify_id::CHAR(22), -- Explicitly casts existing values to CHAR(22)
    ALTER COLUMN daily_rank TYPE SMALLINT USING daily_rank::SMALLINT, -- smallint: Custom rank (not from Spotify)
    ALTER COLUMN daily_movement TYPE SMALLINT USING daily_movement::SMALLINT, -- smallint: Custom daily rank movement
    ALTER COLUMN weekly_movement TYPE SMALLINT USING weekly_movement::SMALLINT, -- smallint: Custom weekly rank movement
    ALTER COLUMN country TYPE CHAR(2) USING country::CHAR(2), -- string: ISO 3166-1 alpha-2 country code
    ALTER COLUMN snapshot_date TYPE DATE USING NULLIF(snapshot_date, '')::DATE, -- date: Snapshot date for the metrics
    ALTER COLUMN popularity TYPE SMALLINT USING popularity::SMALLINT, -- integer: Popularity (0–100)
    ALTER COLUMN is_explicit TYPE BOOLEAN USING is_explicit::BOOLEAN, -- boolean: True if track is marked explicit
    ALTER COLUMN duration_ms TYPE INTEGER USING duration_ms::INTEGER, -- integer: Track duration in milliseconds
    ALTER COLUMN album_name TYPE TEXT, -- string: Album name
    ALTER COLUMN album_release_date TYPE DATE USING NULLIF(album_release_date, '')::DATE, -- date: Album release date
    ALTER COLUMN danceability TYPE REAL USING danceability::REAL, -- float: 0.0–1.0; dance suitability
    ALTER COLUMN energy TYPE REAL USING energy::REAL, -- float: 0.0–1.0; perceptual intensity
    ALTER COLUMN key TYPE SMALLINT USING key::SMALLINT, -- integer: Musical key (-1 = unknown, 0 = C, ..., 11 = B)
    ALTER COLUMN loudness TYPE REAL USING loudness::REAL, -- float: Average loudness in dB
    ALTER COLUMN mode TYPE BOOLEAN USING mode::BOOLEAN, -- boolean: 0 = minor, 1 = major
    ALTER COLUMN speechiness TYPE REAL USING speechiness::REAL, -- float: 0.0–1.0; presence of spoken words
    ALTER COLUMN acousticness TYPE REAL USING acousticness::REAL, -- float: 0.0–1.0; confidence the track is acoustic
    ALTER COLUMN instrumentalness TYPE REAL USING instrumentalness::REAL, -- float: 0.0–1.0; likelihood of being instrumental
    ALTER COLUMN liveness TYPE REAL USING liveness::REAL, -- float: 0.0–1.0; probability the track is live
    ALTER COLUMN valence TYPE REAL USING valence::REAL, -- float: 0.0–1.0; musical positiveness
    ALTER COLUMN tempo TYPE REAL USING tempo::REAL, -- float: Beats per minute
    ALTER COLUMN time_signature TYPE SMALLINT USING time_signature::SMALLINT;

/*---------------------------------------------------------------------------------------------------
------------------------UPDATE -> MATCH name AND artist for the same spotify ID----------------------
-----------------------------NOTE: USING THE MOST RECENT NOT NULL VALUE------------------------------
---------------------------------------------------------------------------------------------------*/

WITH name_artists_ranked AS (
    SELECT
        spotify_id,
        name,
        artists,
        snapshot_date,
        id,
        -- Rank for 'name', prioritizing non-null, then by date, then by id
        ROW_NUMBER() OVER (
            PARTITION BY spotify_id
            ORDER BY
                CASE
                    WHEN name IS NOT NULL THEN 0 -- Non-null strings get rank 0 (highest priority)
                    ELSE 1 -- Null strings get rank 1 (lower priority)
                END ASC,
                snapshot_date DESC, -- Then by most recent snapshot date
                id DESC              -- Then by id for tie-breaking
        ) AS rn_name,
        -- Rank for 'artists', similarly prioritizing non-null
        ROW_NUMBER() OVER (
            PARTITION BY spotify_id
            ORDER BY
                CASE
                    WHEN artists IS NOT NULL THEN 0
                    ELSE 1
                END ASC,
                snapshot_date DESC,
                id DESC
        ) AS rn_artists
    FROM spotify_songs_staging
),
best_name_artists AS (
    SELECT
        spotify_id,
        -- Select the 'name' from the record with rn_name = 1 (the highest priority name)
        MAX(CASE WHEN rn_name = 1 THEN name ELSE NULL END) AS best_name,
        -- Select the 'artists' from the record with rn_artists = 1 (the highest priority artists)
        MAX(CASE WHEN rn_artists = 1 THEN artists ELSE NULL END) AS best_artists
    FROM name_artists_ranked
    GROUP BY spotify_id
)
UPDATE spotify_songs_staging AS target
SET
    name = source.best_name,
    artists = source.best_artists
FROM best_name_artists AS source
WHERE
    target.spotify_id = source.spotify_id
    AND (
        target.name IS DISTINCT FROM source.best_name OR
        target.artists IS DISTINCT FROM source.best_artists
    );

/*---------------------------------------------------------------------------------------------------
------------------------------------UPDATE -> SONG PARAMETER-----------------------------------------
-----------------------------NOTE: USING THE MOST RECENT NOT NULL VALUE------------------------------
---------------------------------------------------------------------------------------------------*/

WITH row_validity_scores AS (
    SELECT
        spotify_id,
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
        time_signature,
        snapshot_date,
        id,
        (CASE WHEN (is_explicit IS NULL OR is_explicit IN (TRUE, FALSE)) THEN 1 ELSE 0 END) +
        (CASE WHEN (duration_ms IS NULL OR duration_ms > 0) THEN 1 ELSE 0 END) +
        (CASE WHEN (danceability IS NULL OR danceability BETWEEN 0.0 AND 1.0) THEN 1 ELSE 0 END) +
        (CASE WHEN (energy IS NULL OR energy BETWEEN 0.0 AND 1.0) THEN 1 ELSE 0 END) +
        (CASE WHEN (key IS NULL OR key BETWEEN -1 AND 11) THEN 1 ELSE 0 END) +
        (CASE WHEN (loudness IS NULL OR loudness BETWEEN -60.0 AND 0.0) THEN 1 ELSE 0 END) +
        (CASE WHEN (mode IS NULL OR mode IN (TRUE, FALSE)) THEN 1 ELSE 0 END) +
        (CASE WHEN (speechiness IS NULL OR speechiness BETWEEN 0.0 AND 1.0) THEN 1 ELSE 0 END) +
        (CASE WHEN (acousticness IS NULL OR acousticness BETWEEN 0.0 AND 1.0) THEN 1 ELSE 0 END) +
        (CASE WHEN (instrumentalness IS NULL OR instrumentalness BETWEEN 0.0 AND 1.0) THEN 1 ELSE 0 END) +
        (CASE WHEN (liveness IS NULL OR liveness BETWEEN 0.0 AND 1.0) THEN 1 ELSE 0 END) +
        (CASE WHEN (valence IS NULL OR valence BETWEEN 0.0 AND 1.0) THEN 1 ELSE 0 END) +
        (CASE WHEN (tempo IS NULL OR tempo > 0) THEN 1 ELSE 0 END) +
        (CASE WHEN (time_signature IS NULL OR time_signature BETWEEN 3 AND 7) THEN 1 ELSE 0 END) AS validity_score
    FROM
        spotify_songs_staging
),
most_recent_best_parameter AS (
    SELECT
        spotify_id,
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
        time_signature,
        ROW_NUMBER() OVER(
            PARTITION BY spotify_id
            ORDER BY
                validity_score DESC, -- Prioritize rows with a higher validity score (more valid columns)
                snapshot_date DESC,  -- Then, among equally valid rows, pick the most recent
                id DESC              -- Finally, use id as a tie-breaker
        ) as rn
    FROM
        row_validity_scores
)
UPDATE spotify_songs_staging AS target
SET
    is_explicit = source.is_explicit,
    duration_ms = source.duration_ms,
    album_name = source.album_name,
    album_release_date = source.album_release_date,
    danceability = source.danceability,
    energy = source.energy,
    key = source.key,
    loudness = source.loudness,
    mode = source.mode,
    speechiness = source.speechiness,
    acousticness = source.acousticness,
    instrumentalness = source.instrumentalness,
    liveness = source.liveness,
    valence = source.valence,
    tempo = source.tempo,
    time_signature = source.time_signature
FROM
    most_recent_best_parameter AS source
WHERE
    target.spotify_id = source.spotify_id
    AND source.rn = 1
    AND (
        (target.is_explicit IS DISTINCT FROM source.is_explicit) OR
        (target.duration_ms IS DISTINCT FROM source.duration_ms) OR
        (target.album_name IS DISTINCT FROM source.album_name) OR
        (target.album_release_date IS DISTINCT FROM source.album_release_date) OR
        (target.danceability IS DISTINCT FROM source.danceability) OR
        (target.energy IS DISTINCT FROM source.energy) OR
        (target.key IS DISTINCT FROM source.key) OR
        (target.loudness IS DISTINCT FROM source.loudness) OR
        (target.mode IS DISTINCT FROM source.mode) OR
        (target.speechiness IS DISTINCT FROM source.speechiness) OR
        (target.acousticness IS DISTINCT FROM source.acousticness) OR
        (target.instrumentalness IS DISTINCT FROM source.instrumentalness) OR
        (target.liveness IS DISTINCT FROM source.liveness) OR
        (target.valence IS DISTINCT FROM source.valence) OR
        (target.tempo IS DISTINCT FROM source.tempo) OR
        (target.time_signature IS DISTINCT FROM source.time_signature)
    );

/*---------------------------------------------------------------------------------------------------
------------------------------------UPDATE -> country (NULL to 'ZZ' for Global)----------------------
---------------------------------------------------------------------------------------------------*/
-- If country is NULL, it indicates a 'Global Top 50' playlist entry.
-- This updates NULL country values to 'ZZ' for consistent global representation.
-- Reference: https://www.kaggle.com/datasets/asaniczka/top-spotify-songs-in-73-countries-daily-updated/data

UPDATE spotify_songs_staging AS target
SET country = 'ZZ'
WHERE country IS NULL;

/*---------------------------------------------------------------------------------------------------
------------------------------------DELETE-> NULL names----------------------------------------------
---------------------------------------------------------------------------------------------------*/
-- Deletes rows where the song name is NULL. It's noted that NULL artists are
-- often associated with NULL names, making these rows less useful for analysis.
-- album_name (792 NULLs) and album_release_date (630 NULLs) will remain NULL
-- for data integrity purposes, as they are not critical for core analyses.

DELETE FROM spotify_songs_staging
WHERE name IS NULL;