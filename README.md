# Musical World - A Stylish Music Player

Musical World is a feature-packed music player application built with Python, designed to provide a seamless and visually appealing experience for music lovers. This application incorporates a modern user interface, smooth music playback capabilities, and MySQL database integration for effective playlist management.

---

## Features:

- **Music Playback**: Supports MP3 files with controls for play, stop, next, and previous tracks.
- **Playlist Management**: Add, delete, and organize songs using a MySQL database.
- **Song Metadata**: Displays details such as title, artist, and album.
- **Stylish Interface**: Built with `Tkinter`, offering hover effects, custom buttons, and an intuitive design.
- **Volume Control**: Adjustable volume settings with saved preferences for convenience.
- **Progress Bar**: Real-time playback progress tracking.

---

## Tech Stack 🛠️

- **Python**: Core programming language.
- **Pygame**: For music playback functionality.
- **Tkinter**: For creating the graphical user interface.
- **MySQL**: Backend database for managing song data.

---

## Installation:

Follow these steps to set up and run the project:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/<your-username>/musical-world.git
   ```

2. **Install Dependencies**:
   ```bash
   pip install mysql-connector-python pygame
   ```

3. **Set Up MySQL Database**:
   - Create a database named `media_player`.
   - Use the following schema to create the `songs` table:
     ```sql
     CREATE TABLE songs (
         id INT AUTO_INCREMENT PRIMARY KEY,
         title VARCHAR(255),
         path TEXT,
         artist VARCHAR(255),
         album VARCHAR(255)
     );
     ```

4. **Run the Application**:
   ```bash
   python music_player.py
   ```

---

## Usage:

1. **Add Songs**:
   - Use the "Add Song" button to upload MP3 files. Input artist and album details when prompted.
   - Songs are stored in the database and displayed in the playlist.

2. **Play Songs**:
   - Select a song from the playlist and click "Play" to enjoy your music.

3. **Manage Playlist**:
   - Use "Delete Song" to remove tracks from the playlist.

4. **Navigation**:
   - Switch between songs using "Next" and "Previous" buttons.

5. **Volume Adjustment**:
   - Use the volume slider to set your preferred audio level.

---

## Future Enhancements:

- Add support for more audio formats like WAV and FLAC.
- Implement user authentication for personalized playlists.
- Introduce themes for a customizable user interface.
- Enhance metadata retrieval using online APIs.


