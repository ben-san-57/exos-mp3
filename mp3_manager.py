import os
import shutil
from mutagen.id3 import ID3, APIC
from music_track import MusicTrack
from database import MusicDatabase

class MP3Manager:
    def __init__(self):
        self.tracks = []
        self.db = MusicDatabase()
        self.temp_album_art_dir = "temp_album_art"
        os.makedirs(self.temp_album_art_dir, exist_ok=True)

    def scan_directory(self, directory):
        """Analyse un répertoire et récupère les métadonnées MP3"""
        self.tracks.clear()
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(".mp3"):
                    path = os.path.join(root, file)
                    if self.db.track_exists(path):
                        print(f"Fichier déjà importé : {file}")
                        continue

                    try:
                        audio = ID3(path)
                        title = str(audio.get("TIT2", ["Inconnu"])[0])
                        artist = str(audio.get("TPE1", ["Inconnu"])[0])
                        album = str(audio.get("TALB", ["Inconnu"])[0])
                        genre = str(audio.get("TCON", ["Inconnu"])[0])
                        duration = int(os.path.getsize(path) / 16000)

                        album_art_path = None
                        for tag in audio.getall("APIC"):
                            if isinstance(tag, APIC):
                                image_data = tag.data
                                album_art_filename = f"{os.path.splitext(os.path.basename(path))[0]}.jpg"
                                album_art_path = os.path.join(self.temp_album_art_dir, album_art_filename)
                                with open(album_art_path, "wb") as img_file:
                                    img_file.write(image_data)
                            
                                break

                        track = MusicTrack(path, title, artist, album, genre, duration, album_art_path)
                        self.tracks.append(track)
                        self.db.add_track(track)
                    except Exception as e:
                        print(f"Erreur lors de la lecture de {file}: {e}")
        return self.tracks

    def sort_by_album(self):
        """Trie les pistes par album"""
        self.tracks.sort(key=lambda x: x.album)

    def sort_by_genre(self):
        """Trie les pistes par genre"""
        self.tracks.sort(key=lambda x: x.genre)

    def copy_by_album(self, destination):
        """Copie les fichiers triés par album"""
        self.sort_by_album()
        for track in self.tracks:
            target_dir = os.path.join(destination, "Par_Album", track.album)
            os.makedirs(target_dir, exist_ok=True)
            shutil.copy(track.path, os.path.join(target_dir, os.path.basename(track.path)))

    def copy_by_genre(self, destination):
        """Copie les fichiers triés par genre"""
        self.sort_by_genre()
        for track in self.tracks:
            target_dir = os.path.join(destination, "Par_Genre", track.genre)
            os.makedirs(target_dir, exist_ok=True)
            shutil.copy(track.path, os.path.join(target_dir, os.path.basename(track.path)))

    def get_db_tracks(self):
        return self.db.get_all_tracks()