from abc import ABC, abstractmethod

class MediaItem(ABC):
    def __init__(self, title, duration):
        self._title = title
        self._duration = duration  # en secondes

    @property
    def title(self):
        return self._title

    @property
    def duration(self):
        return self._duration

    def get_formatted_duration(self):
        mins = self._duration // 60
        secs = self._duration % 60
        return f"{mins:02d}:{secs:02d}"

    @abstractmethod
    def info(self):
        pass