from media_item import MediaItem
import os

class MusicTrack(MediaItem):
    def __init__(self, path, title, artist, album, genre, duration, album_art=None):
        super().__init__(title, duration)
        self._path = path
        self._artist = artist
        self._album = album
        self._genre = genre or "Inconnu"
        self._album_art = album_art

    @property
    def path(self):
        return self._path

    @property
    def artist(self):
        return self._artist

    @property
    def album(self):
        return self._album

    @property
    def genre(self):
        return self._genre

    @property
    def album_art(self):
        return self._album_art

    def info(self):
        return f"{self.title} - {self.artist} ({self.album}, {self.genre}) [{self.get_formatted_duration()}]"