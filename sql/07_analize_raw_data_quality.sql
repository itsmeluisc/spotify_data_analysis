/*---------------------------------------------------
-----------------------------------------------------
--ANALIZING DATA QUALITY 
--NULL AND EMPTY STRINGS VALUES (INCLUDING TRAILING WHITE SPACES)
CONCLUSION: there are not null values in any row but there are a lot of empty
strings in artist (29), country (28908), album name (822), name (30) and album realease data(659)
-----------------------------------------------------
----------------------------------------------------*/

SELECT
    'spotify_id' AS variable_name,
    COUNT(CASE WHEN spotify_id = '' OR TRIM(spotify_id) = '' THEN 1 ELSE NULL END) AS empty_string_count,
    COUNT(CASE WHEN spotify_id IS NULL THEN 1 ELSE NULL END) AS null_count
    --TRIM() removes any leading or trailing whitespace (spaces, tabs, newlines) from a string.
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'name' AS variable_name,
    COUNT(CASE WHEN name = '' OR TRIM(name) = '' THEN 1 ELSE NULL END) AS empty_string_count,
    COUNT(CASE WHEN name IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'artists' AS variable_name,
    COUNT(CASE WHEN artists = '' OR TRIM(artists) = '' THEN 1 ELSE NULL END) AS empty_string_count,
    COUNT(CASE WHEN artists IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'daily_rank' AS variable_name,
    COUNT(CASE WHEN daily_rank = '' OR TRIM(daily_rank) = '' THEN 1 ELSE NULL END) AS empty_string_count,
    COUNT(CASE WHEN daily_rank IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'daily_movement' AS variable_name,
    COUNT(CASE WHEN daily_movement = '' OR TRIM(daily_movement) = '' THEN 1 ELSE NULL END) AS empty_string_count,
    COUNT(CASE WHEN daily_movement IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'weekly_movement' AS variable_name,
    COUNT(CASE WHEN weekly_movement = '' OR TRIM(weekly_movement) = '' THEN 1 ELSE NULL END) AS empty_string_count,
    COUNT(CASE WHEN weekly_movement IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'country' AS variable_name,
    COUNT(CASE WHEN country = '' OR TRIM(country) = '' THEN 1 ELSE NULL END) AS empty_string_count,
    COUNT(CASE WHEN country IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'snapshot_date' AS variable_name,
    COUNT(CASE WHEN snapshot_date = '' OR TRIM(snapshot_date) = '' THEN 1 ELSE NULL END) AS empty_string_count,
    COUNT(CASE WHEN snapshot_date IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'popularity' AS variable_name,
    COUNT(CASE WHEN popularity = '' OR TRIM(popularity) = '' THEN 1 ELSE NULL END) AS empty_string_count,
    COUNT(CASE WHEN popularity IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'is_explicit' AS variable_name,
    COUNT(CASE WHEN is_explicit = '' OR TRIM(is_explicit) = '' THEN 1 ELSE NULL END) AS empty_string_count,
    COUNT(CASE WHEN is_explicit IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'duration_ms' AS variable_name,
    COUNT(CASE WHEN duration_ms = '' OR TRIM(duration_ms) = '' THEN 1 ELSE NULL END) AS empty_string_count,
    COUNT(CASE WHEN duration_ms IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'album_name' AS variable_name,
    COUNT(CASE WHEN album_name = '' OR TRIM(album_name) = '' THEN 1 ELSE NULL END) AS empty_string_count,
    COUNT(CASE WHEN album_name IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'album_release_date' AS variable_name,
    COUNT(CASE WHEN album_release_date = '' OR TRIM(album_release_date) = '' THEN 1 ELSE NULL END) AS empty_string_count,
    COUNT(CASE WHEN album_release_date IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'danceability' AS variable_name,
    COUNT(CASE WHEN danceability = '' OR TRIM(danceability) = '' THEN 1 ELSE NULL END) AS empty_string_count,
    COUNT(CASE WHEN danceability IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'energy' AS variable_name,
    COUNT(CASE WHEN energy = '' OR TRIM(energy) = '' THEN 1 ELSE NULL END) AS empty_string_count,
    COUNT(CASE WHEN energy IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'key' AS variable_name,
    COUNT(CASE WHEN key = '' OR TRIM(key) = '' THEN 1 ELSE NULL END) AS empty_string_count,
    COUNT(CASE WHEN key IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'loudness' AS variable_name,
    COUNT(CASE WHEN loudness = '' OR TRIM(loudness) = '' THEN 1 ELSE NULL END) AS empty_string_count,
    COUNT(CASE WHEN loudness IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'mode' AS variable_name,
    COUNT(CASE WHEN mode = '' OR TRIM(mode) = '' THEN 1 ELSE NULL END) AS empty_string_count,
    COUNT(CASE WHEN mode IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'speechiness' AS variable_name,
    COUNT(CASE WHEN speechiness = '' OR TRIM(speechiness) = '' THEN 1 ELSE NULL END) AS empty_string_count,
    COUNT(CASE WHEN speechiness IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'acousticness' AS variable_name,
    COUNT(CASE WHEN acousticness = '' OR TRIM(acousticness) = '' THEN 1 ELSE NULL END) AS empty_string_count,
    COUNT(CASE WHEN acousticness IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'instrumentalness' AS variable_name,
    COUNT(CASE WHEN instrumentalness = '' OR TRIM(instrumentalness) = '' THEN 1 ELSE NULL END) AS empty_string_count,
    COUNT(CASE WHEN instrumentalness IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'liveness' AS variable_name,
    COUNT(CASE WHEN liveness = '' OR TRIM(liveness) = '' THEN 1 ELSE NULL END) AS empty_string_count,
    COUNT(CASE WHEN liveness IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'valence' AS variable_name,
    COUNT(CASE WHEN valence = '' OR TRIM(valence) = '' THEN 1 ELSE NULL END) AS empty_string_count,
    COUNT(CASE WHEN valence IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'tempo' AS variable_name,
    COUNT(CASE WHEN tempo = '' OR TRIM(tempo) = '' THEN 1 ELSE NULL END) AS empty_string_count,
    COUNT(CASE WHEN tempo IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'time_signature' AS variable_name,
    COUNT(CASE WHEN time_signature = '' OR TRIM(time_signature) = '' THEN 1 ELSE NULL END) AS empty_string_count,
    COUNT(CASE WHEN time_signature IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging;