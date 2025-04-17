
from app import app
import os

# Not sure how to install this come back to later 
# pip install pygame


if __name__ == "__main__":
    
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
    
    # app.run(debug="True", ssl_context='adhoc')
    app.run(debug="True",use_reloader=True, ssl_context=('cert.pem', 'key.pem'))


import tkinter as tk
from tkinter import ttk
import time
import threading
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Load lo-fi music (you must have a local mp3 file)
MUSIC_FILE = "lofi.mp3"

class MeditationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🧘 Meditation Timer")

        self.is_running = False
        self.music_on = False
        self.remaining_seconds = 600  # 10 minutes

        # Timer Label
        self.timer_label = tk.Label(root, text="10:00", font=("Helvetica", 48))
        self.timer_label.pack(pady=20)

        # Progress Bar
        self.progress = ttk.Progressbar(root, length=300, mode='determinate')
        self.progress.pack(pady=10)

        # Start Button
        self.start_button = tk.Button(root, text="Start Meditation", command=self.start_timer)
        self.start_button.pack(pady=10)

        # Music Toggle Button
        self.music_button = tk.Button(root, text="🔈 Music: OFF", command=self.toggle_music)
        self.music_button.pack(pady=10)

    def toggle_music(self):
        self.music_on = not self.music_on
        if self.music_on:
            pygame.mixer.music.load(MUSIC_FILE)
            pygame.mixer.music.play(-1)  # Loop indefinitely
            self.music_button.config(text="🔊 Music: ON")
        else:
            pygame.mixer.music.stop()
            self.music_button.config(text="🔈 Music: OFF")

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.start_button.config(state=tk.DISABLED)
            threading.Thread(target=self.run_timer, daemon=True).start()

    def run_timer(self):
        total_seconds = 600
        while self.remaining_seconds > 0:
            mins, secs = divmod(self.remaining_seconds, 60)
            self.timer_label.config(text=f"{mins:02}:{secs:02}")
            self.progress['value'] = ((total_seconds - self.remaining_seconds) / total_seconds) * 100
            self.remaining_seconds -= 1
            time.sleep(1)

        self.timer_label.config(text="🧘 Done!")
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.remaining_seconds = 600  # Reset
        self.progress['value'] = 0
        if self.music_on:
            pygame.mixer.music.stop()
            self.music_button.config(text="🔈 Music: OFF")
            self.music_on = False

# Run app
if __name__ == "__main__":
    root = tk.Tk()
    app = MeditationApp(root)
    root.mainloop()
