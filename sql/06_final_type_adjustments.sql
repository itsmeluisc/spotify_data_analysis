-- sql/06_final_type_adjustments.sql
-- Brief Description: Performs final type adjustments for specific columns (is_explicit, mode)
-- in the spotify_songs_2024 table, casting them from BOOLEAN to INTEGER.

/*---------------------------------------------------------------------------------------------------
------------------------------FINAL TYPE ADJUSTMENTS (e.g., BOOLEAN to INTEGER)--------------------
---------------------------------------------------------------------------------------------------*/

ALTER TABLE spotify_songs_2024
ALTER COLUMN is_explicit TYPE INTEGER
USING is_explicit::int;

ALTER TABLE spotify_songs_2024
ALTER COLUMN mode TYPE INTEGER
USING mode::int;