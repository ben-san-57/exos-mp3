from media_item import MediaItem

class MusicTrack(MediaItem):
    def __init__(self, path, title, artist, album, genre, duration):
        super().__init__(title, duration)
        self._path = path
        self._artist = artist
        self._album = album
        self._genre = genre

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
        return self._genre or "Inconnu"

    def info(self):
        return f"{self.title} - {self.artist} ({self.album}, {self.genre}) [{self.get_formatted_duration()}]"