import sqlite3
import os

class MusicDatabase:
    def __init__(self, db_path="music.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS tracks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    artist TEXT,
                    album TEXT,
                    genre TEXT,
                    duration INTEGER,
                    path TEXT UNIQUE
                )
            """)

    def add_track(self, track):
        try:
            with self.conn:
                self.conn.execute("""
                    INSERT OR IGNORE INTO tracks (title, artist, album, genre, duration, path)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (track.title, track.artist, track.album, track.genre, track.duration, track.path))
        except Exception as e:
            print(f"Erreur lors de l'insertion : {e}")

    def get_all_tracks(self):
        return self.conn.execute("SELECT title, artist, album, genre, duration FROM tracks").fetchall()

    def track_exists(self, path):
        result = self.conn.execute("SELECT 1 FROM tracks WHERE path = ?", (path,)).fetchone()
        return result is not None