-- sql/05_create_2024_table.sql
-- Brief Description: Creates a new table named spotify_songs_2024 containing only data from
-- the year 2024, derived from the main spotify_songs table. This provides a focused subset
-- for yearly analysis.

/*---------------------------------------------------------------------------------------------------
------------------------------------CREATE TABLE FOR YEAR 2024---------------------------------------
---------------------------------------------------------------------------------------------------*/

-- Drop if exists for idempotency
DROP TABLE IF EXISTS spotify_songs_2024;

CREATE TABLE spotify_songs_2024 AS
SELECT *
FROM
    spotify_songs
WHERE
    snapshot_date >= DATE '2024-01-01' AND snapshot_date < DATE '2025-01-01';