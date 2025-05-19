import os
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
from mp3_manager import MP3Manager

class MP3ManagerUI:
    def __init__(self, root):
        self.manager = MP3Manager()

        self.root = root
        self.root.title("Gestionnaire de Fichiers MP3")
        self.root.geometry("900x600")
        self.root.configure(bg="#1e1e2f")

        self.create_widgets()

    def create_widgets(self):
        title = Label(
            self.root,
            text="🎶 Gestionnaire de Fichiers MP3",
            font=("Helvetica", 18, "bold"),
            bg="#1e1e2f",
            fg="#ffffff"
        )
        title.pack(pady=20)

        self.import_btn = Button(
            self.root,
            text="📁 Importer Répertoire",
            width=25,
            command=self.import_directory,
            bg="#4e54c8",
            fg="white",
            font=("Arial", 12),
            relief=FLAT,
            bd=0
        )
        self.import_btn.pack(pady=10)

        self.organize_frame = Frame(self.root, bg="#1e1e2f")
        self.organize_frame.pack(pady=10)

        self.album_btn = Button(
            self.organize_frame,
            text="📁 Organiser par Album",
            width=20,
            command=self.organize_by_album,
            bg="#ff6f61",
            fg="white",
            font=("Arial", 12),
            relief=FLAT,
            state=DISABLED
        )
        self.album_btn.grid(row=0, column=0, padx=10)

        self.genre_btn = Button(
            self.organize_frame,
            text="📁 Organiser par Genre",
            width=20,
            command=self.organize_by_genre,
            bg="#6ab04c",
            fg="white",
            font=("Arial", 12),
            relief=FLAT,
            state=DISABLED
        )
        self.genre_btn.grid(row=0, column=1, padx=10)

        list_and_image_frame = Frame(self.root, bg="#1e1e2f")
        list_and_image_frame.pack(pady=10, fill=BOTH, expand=True)

        self.listbox = Listbox(
            list_and_image_frame,
            height=15,
            width=70,
            bg="#2a2a3d",
            fg="white",
            selectbackground="#4e54c8",
            font=("Courier", 10)
        )
        self.listbox.pack(side=LEFT, padx=10, fill=Y)
        self.listbox.bind("<<ListboxSelect>>", self.show_album_art)

        self.album_art_label = Label(list_and_image_frame, bg="#1e1e2f")
        self.album_art_label.pack(side=RIGHT, padx=10)

        self.view_btn = Button(
            self.root,
            text="📚 Voir Base de Données",
            width=25,
            command=self.view_database,
            bg="#feca57",
            fg="black",
            font=("Arial", 12),
            relief=FLAT
        )
        self.view_btn.pack(pady=5)

    def import_directory(self):
        directory = filedialog.askdirectory()
        if not directory:
            return

        tracks = self.manager.scan_directory(directory)
        self.listbox.delete(0, END)

        for track in tracks:
            self.listbox.insert(END, track.info())

        self.album_btn.config(state=NORMAL)
        self.genre_btn.config(state=NORMAL)
        messagebox.showinfo("Succès", f"{len(tracks)} fichiers MP3 chargés.")

    def organize_by_album(self):
        dest = filedialog.askdirectory(title="Sélectionnez le dossier de destination")
        if dest:
            self.manager.copy_by_album(dest)
            messagebox.showinfo("Succès", "Fichiers organisés par album !")

    def organize_by_genre(self):
        dest = filedialog.askdirectory(title="Sélectionnez le dossier de destination")
        if dest:
            self.manager.copy_by_genre(dest)
            messagebox.showinfo("Succès", "Fichiers organisés par genre !")

    def view_database(self):
        self.listbox.delete(0, END)
        tracks = self.manager.get_db_tracks()
        for track in tracks:
            title, artist, album, genre, duration = track
            mins = duration // 60
            secs = duration % 60
            formatted_duration = f"{mins:02d}:{secs:02d}"
            self.listbox.insert(END, f"{title} - {artist} ({album}, {genre}) [{formatted_duration}]")

    def show_album_art(self, event):
        selected_index = self.listbox.curselection()
        if not selected_index:
            return

        index = selected_index[0]
        track = self.manager.tracks[index]

        if track.album_art and os.path.exists(track.album_art):
            try:
                img = Image.open(track.album_art)
                img.thumbnail((200, 200))
                photo = ImageTk.PhotoImage(img)
                self.album_art_label.configure(image=photo)
                self.album_art_label.image = photo
            except Exception as e:
                print(f"Erreur de chargement de l'image : {e}")
                self.album_art_label.configure(image="")
        else:
            self.album_art_label.configure(image="")