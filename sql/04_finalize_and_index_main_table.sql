-- sql/04_finalize_and_index_main_table.sql
-- Brief Description: Renames the spotify_songs_staging table to its final, production-ready name,
-- spotify_songs. It also adds essential indexes to the spotify_songs table to optimize
-- query performance for subsequent analysis.

/*---------------------------------------------------------------------------------------------------
------------------------------------ALTER TABLE -> RENAME TO FINAL TABLE-----------------------------
---------------------------------------------------------------------------------------------------*/

ALTER TABLE spotify_songs_staging RENAME TO spotify_songs;


/*---------------------------------------------------------------------------------------------------
------------------------------------ADD INDEXES TO FINAL TABLE---------------------------------------
---------------------------------------------------------------------------------------------------*/
-- Adding indexes to the final table for query performance
CREATE INDEX IF NOT EXISTS idx_spotify_songs_id ON spotify_songs (spotify_id);
CREATE INDEX IF NOT EXISTS idx_spotify_songs_country ON spotify_songs (country);
CREATE INDEX IF NOT EXISTS idx_spotify_songs_snapshot_date ON spotify_songs (snapshot_date);
CREATE INDEX IF NOT EXISTS idx_spotify_songs_popularity ON spotify_songs (popularity);