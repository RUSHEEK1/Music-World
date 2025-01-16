import mysql.connector
import pygame
import os
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import json

# Database connection function
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Change as per your setup
        password="root",  # Change as per your setup
        database="media_player"  # Change as per your setup
    )

# Insert song into the database
def insert_song(title, path, artist=None, album=None):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO songs (title, path, artist, album) VALUES (%s, %s, %s, %s)",
                   (title, path, artist, album))
    connection.commit()
    cursor.close()
    connection.close()

# Fetch songs from the database
def fetch_songs():
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM songs")
    songs = cursor.fetchall()
    cursor.close()
    connection.close()
    return songs

# Delete song from the database by ID
def delete_song_by_id(song_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM songs WHERE id = %s", (song_id,))
    connection.commit()
    cursor.close()
    connection.close()

class MediaPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Stylish Media Player")
        self.root.geometry("800x600")
        self.root.configure(bg="#2C3E50")

        pygame.mixer.init()

        # Load volume from config file
        self.volume = self.load_volume()
        pygame.mixer.music.set_volume(self.volume)

        # Title Label
        title_label = Label(root, text="Musical World", font=("Helvetica", 24, "bold"), bg="#2C3E50", fg="#ECF0F1")
        title_label.pack(pady=20)

        # Playlist Treeview
        self.tree_frame = Frame(root, bg="#2C3E50", bd=2, relief=GROOVE)
        self.tree_frame.pack(pady=20, padx=20, fill=BOTH, expand=True)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background="#34495E", foreground="white")
        style.configure("Treeview", font=("Helvetica", 10), rowheight=30, background="#ECF0F1",
                        fieldbackground="#ECF0F1")

        self.tree = ttk.Treeview(self.tree_frame, columns=("Title", "Artist", "Album", "Path"), show='headings', height=8)
        self.tree.heading("Title", text="Title")
        self.tree.heading("Artist", text="Artist")
        self.tree.heading("Album", text="Album")
        self.tree.heading("Path", text="Path")
        self.tree.column("Title", width=250)
        self.tree.column("Artist", width=100)
        self.tree.column("Album", width=100)
        self.tree.column("Path", width=250)
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)

        # Add Scrollbar to Playlist
        self.scrollbar = ttk.Scrollbar(self.tree_frame, orient=VERTICAL, command=self.tree.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.tree.config(yscrollcommand=self.scrollbar.set)

        self.load_songs()

        # Control variables
        self.current_song_index = None
        self.is_playing = False  # Track playback state

        # Control Buttons Frame
        controls_frame = Frame(root, bg="#2C3E50")
        controls_frame.pack(pady=20)

        # Adding buttons with custom styling and hover effects
        self.play_button = self.create_button(controls_frame, "Play", self.play_song, "#27AE60", "▶")
        self.stop_button = self.create_button(controls_frame, "Stop", self.stop_song, "#E74C3C", "■")
        self.add_button = self.create_button(controls_frame, "Add Song", self.add_song, "#2980B9", "+")
        self.delete_button = self.create_button(controls_frame, "Delete Song", self.delete_selected_song, "#C0392B", "−")
        self.next_button = self.create_button(controls_frame, "Next", self.next_song, "#F39C12", "➡️")
        self.previous_button = self.create_button(controls_frame, "Previous", self.previous_song, "#8E44AD", "⬅️")

        # Volume Control
        volume_frame = Frame(root, bg="#2C3E50")
        volume_frame.pack(pady=10)

        Label(volume_frame, text="Volume:", font=("Helvetica", 10), bg="#2C3E50", fg="white").pack(side=LEFT)
        self.volume_scale = Scale(volume_frame, from_=0, to=1, resolution=0.1, orient=HORIZONTAL,
                                  command=self.set_volume,
                                  bg="#34495E", fg="white", highlightthickness=0)
        self.volume_scale.set(self.volume)
        self.volume_scale.pack(side=LEFT, padx=10)

        # Progress bar for song playback
        self.progress_var = DoubleVar()
        self.progress_bar = ttk.Progressbar(root, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(pady=10, fill=X, padx=20)

        self.update_progress()  # Start updating the progress bar

    def create_button(self, parent, text, command, bg_color, symbol):
        button = Button(parent, text=symbol, command=command, font=("Helvetica", 12, "bold"),
                        bg=bg_color, fg="white", width=4, relief=FLAT)
        button.bind("<Enter>", lambda e: button.config(bg="#16A085"))  # Hover effect
        button.bind("<Leave>", lambda e: button.config(bg=bg_color))  # Revert effect
        button.grid(row=0, column=len(parent.grid_slaves()), padx=10, pady=5)
        return button

    def add_song(self):
        song_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
        if song_path:
            song_title = os.path.basename(song_path)  # Extract the title from the file path
            artist = input("Enter artist name: ")  # User input for artist
            album = input("Enter album name: ")  # User input for album
            try:
                insert_song(song_title, song_path, artist, album)  # Insert into the database
                self.tree.insert("", "end", values=(song_title, artist, album, song_path))  # Add to the Treeview
                messagebox.showinfo("Success", "Song added to the playlist!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add song: {e}")

    def load_songs(self):
        songs = fetch_songs()  # Fetch songs from the database
        for song in songs:
            self.tree.insert("", "end", values=(song[1], song[3], song[4], song[2]))  # Populate the Treeview

    def play_song(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.current_song_index = self.tree.index(selected_item)
            song_path = self.tree.item(selected_item)['values'][3]
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play()
            self.is_playing = True

    def stop_song(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def get_song_id(self, song_title, song_path):
        connection = connect_to_db()
        cursor = connection.cursor(buffered=True)  # Use a buffered cursor to handle results
        try:
            cursor.execute("SELECT id FROM songs WHERE title = %s AND path = %s", (song_title, song_path))
            result = cursor.fetchone()  # Fetch a single result

            if result:
                return result[0]  # Assuming id is the first column
            else:
                return None
        except Exception as e:
            print(f"Error fetching song ID: {e}")
            return None
        finally:
            cursor.close()
            connection.close()

    def delete_selected_song(self):
        selected_item = self.tree.selection()
        if selected_item:
            song_title = self.tree.item(selected_item)['values'][0]
            song_path = self.tree.item(selected_item)['values'][3]
            song_id = self.get_song_id(song_title, song_path)
            if song_id is not None:
                delete_song_by_id(song_id)  # Delete from the database
                self.tree.delete(selected_item)  # Remove from the Treeview
                messagebox.showinfo("Success", "Song deleted successfully!")
            else:
                messagebox.showerror("Error", "Could not find the song ID.")
        else:
            messagebox.showwarning("Select Song", "Please select a song to delete.")

    def next_song(self):
        if self.current_song_index is not None:
            self.current_song_index += 1
            if self.current_song_index >= len(self.tree.get_children()):
                self.current_song_index = 0  # Loop back to start
            self.play_selected_song()

    def previous_song(self):
        if self.current_song_index is not None:
            self.current_song_index -= 1
            if self.current_song_index < 0:
                self.current_song_index = len(self.tree.get_children()) - 1  # Loop back to end
            self.play_selected_song()

    def play_selected_song(self):
        selected_items = self.tree.get_children()
        if selected_items:
            selected_item = selected_items[self.current_song_index]
            song_path = self.tree.item(selected_item)['values'][3]
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()
            self.is_playing = True

    def set_volume(self, volume):
        self.volume = float(volume)
        pygame.mixer.music.set_volume(self.volume)
        self.save_volume(volume)  # Save volume to config

    def load_volume(self):
        try:
            with open("volume_config.json", "r") as f:
                return json.load(f)["volume"]
        except (FileNotFoundError, json.JSONDecodeError):
            return 0.5  # Default volume

    def save_volume(self, volume):
        with open("volume_config.json", "w") as f:
            json.dump({"volume": float(volume)}, f)

    def update_progress(self):
        if self.is_playing:
            if pygame.mixer.music.get_busy():
                current_pos = pygame.mixer.music.get_pos() / 1000  # Get position in seconds
                self.progress_var.set((current_pos / pygame.mixer.Sound(pygame.mixer.music.get_file()).get_length()) * 100)
            self.root.after(1000, self.update_progress)  # Update every second

if __name__ == "__main__":
    root = Tk()
    player = MediaPlayer(root)
    root.mainloop()
