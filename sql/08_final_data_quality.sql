SELECT
    'spotify_id' AS variable_name,
    COUNT(CASE WHEN spotify_id IS NULL THEN 1 ELSE NULL END) AS null_count
    --TRIM() removes any leading or trailing whitespace (spaces, tabs, newlines) from a string.
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'name' AS variable_name,
    COUNT(CASE WHEN name IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'artists' AS variable_name,
    COUNT(CASE WHEN artists IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'daily_rank' AS variable_name,
    COUNT(CASE WHEN daily_rank IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'daily_movement' AS variable_name,
    COUNT(CASE WHEN daily_movement IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'weekly_movement' AS variable_name,
    COUNT(CASE WHEN weekly_movement IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'country' AS variable_name,
    COUNT(CASE WHEN country IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'snapshot_date' AS variable_name,
    COUNT(CASE WHEN snapshot_date IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'popularity' AS variable_name,
    COUNT(CASE WHEN popularity IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'is_explicit' AS variable_name,
    COUNT(CASE WHEN is_explicit IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'duration_ms' AS variable_name,
    COUNT(CASE WHEN duration_ms IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'album_name' AS variable_name,
    COUNT(CASE WHEN album_name IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'album_release_date' AS variable_name,
    COUNT(CASE WHEN album_release_date IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'danceability' AS variable_name,
    COUNT(CASE WHEN danceability IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'energy' AS variable_name,
    COUNT(CASE WHEN energy IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'key' AS variable_name,
    COUNT(CASE WHEN key IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'loudness' AS variable_name,
    COUNT(CASE WHEN loudness IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'mode' AS variable_name,
    COUNT(CASE WHEN mode IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'speechiness' AS variable_name,
    COUNT(CASE WHEN speechiness IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'acousticness' AS variable_name,
    COUNT(CASE WHEN acousticness IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'instrumentalness' AS variable_name,
    COUNT(CASE WHEN instrumentalness IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'liveness' AS variable_name,
    COUNT(CASE WHEN liveness IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'valence' AS variable_name,
    COUNT(CASE WHEN valence IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'tempo' AS variable_name,
    COUNT(CASE WHEN tempo IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging

UNION ALL

SELECT
    'time_signature' AS variable_name,
    COUNT(CASE WHEN time_signature IS NULL THEN 1 ELSE NULL END) AS null_count
FROM
    spotify_songs_staging;