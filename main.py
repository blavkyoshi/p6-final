import tkinter as tk
from tkinter import ttk
import threading
import time
import os
import pygame  

class MeditationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🧘 Meditation Timer")
        self.root.geometry("400x400")  
        
        
        pygame.mixer.init()
        

        #styling
        style = ttk.Style()
        style.configure("TProgressbar", thickness=20)

        self.is_running = False
        self.music_on = False
        self.remaining_seconds = 600  
        self.total_seconds = 600


        self.timer_frame = tk.Frame(root)
        self.timer_frame.pack(pady=20)
        
        self.controls_frame = tk.Frame(root)
        self.controls_frame.pack(pady=10)
        
        #timer
        self.timer_label = tk.Label(self.timer_frame, text="10:00", font=("Helvetica", 48))
        self.timer_label.pack()

        #progress bar
        self.progress = ttk.Progressbar(root, length=300, mode='determinate', style="TProgressbar")
        self.progress.pack(pady=10)

        #time select
        self.time_frame = tk.Frame(self.controls_frame)
        self.time_frame.pack(pady=10)
        
        tk.Label(self.time_frame, text="Meditation duration:").pack(side=tk.LEFT)
        self.time_options = ["5 minutes", "10 minutes", "15 minutes", "20 minutes", "30 minutes"]
        self.time_var = tk.StringVar(value=self.time_options[1])
        self.time_menu = ttk.Combobox(self.time_frame, textvariable=self.time_var, values=self.time_options, width=10)
        self.time_menu.pack(side=tk.LEFT, padx=5)
        self.time_menu.bind("<<ComboboxSelected>>", self.update_timer)

        #start btn
        self.button_frame = tk.Frame(self.controls_frame)
        self.button_frame.pack(pady=10)
        
        self.start_button = tk.Button(self.button_frame, text="Start Meditation", 
         command=self.start_timer, width=15, height=2,
        bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold"))
        self.start_button.pack(side=tk.LEFT, padx=5)

        #reset btn
        self.reset_button = tk.Button(self.button_frame, text="Reset", 
        command=self.reset_timer, width=10, height=2,
        bg="#f44336", fg="white", font=("Helvetica", 10))
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        #music toggle
        self.music_file = "lofi.mp3"  
        self.music_thread = None
        self.music_button = tk.Button(self.controls_frame, text="🔈 Music: OFF", 
        command=self.toggle_music, width=15)
        self.music_button.pack(pady=10)
        
        #status
        self.status_label = tk.Label(root, text="Ready to meditate", font=("Helvetica", 10, "italic"))
        self.status_label.pack(pady=5)

    def update_timer(self, event=None):
        """Update timer based on selected duration"""
        time_str = self.time_var.get()
        minutes = int(time_str.split()[0])
        self.total_seconds = minutes * 60
        self.remaining_seconds = self.total_seconds
        
        mins, secs = divmod(self.remaining_seconds, 60)
        self.timer_label.config(text=f"{mins:02}:{secs:02}")
        self.progress['value'] = 0

    def toggle_music(self):
        """Toggle background meditation music"""
        if not os.path.exists(self.music_file):
            self.status_label.config(text=f"Music file '{self.music_file}' not found")
            return
            
        self.music_on = not self.music_on
        if self.music_on:
            self.music_button.config(text="🔊 Music: ON")
            self.status_label.config(text="Playing meditation music")
            try:
                pygame.mixer.music.load(self.music_file)
                pygame.mixer.music.play(-1)  
            except Exception as e:
                self.status_label.config(text=f"Music error: {str(e)}")
                self.music_on = False
                self.music_button.config(text="🔈 Music: OFF")
        else:
            pygame.mixer.music.stop()
            self.music_button.config(text="🔈 Music: OFF")
            self.status_label.config(text="Music stopped")
            
    def play_music(self):
        """Play music in a loop while music is enabled"""
        while self.music_on and self.music_thread == threading.current_thread():
            try:
                playsound(self.music_file)
            except Exception as e:
                self.status_label.config(text=f"Music error: {str(e)}")
                self.music_on = False
                self.music_button.config(text="🔈 Music: OFF")
                break

    def start_timer(self):
        """Start the meditation timer"""
        if not self.is_running:
            self.is_running = True
            self.start_button.config(text="Meditating...", state=tk.DISABLED)
            self.status_label.config(text="Meditation in progress")
            threading.Thread(target=self.run_timer, daemon=True).start()

    def reset_timer(self):
        """Reset the meditation timer"""
        self.is_running = False
        self.start_button.config(text="Start Meditation", state=tk.NORMAL)
        self.remaining_seconds = self.total_seconds
        mins, secs = divmod(self.remaining_seconds, 60)
        self.timer_label.config(text=f"{mins:02}:{secs:02}")
        self.progress['value'] = 0
        self.status_label.config(text="Timer reset")

        if self.music_on:
            pygame.mixer.music.stop()
            self.music_on = False
            self.music_button.config(text="🔈 Music: OFF")

    def run_timer(self):
        """Run the timer countdown"""
        while self.remaining_seconds > 0 and self.is_running:
            mins, secs = divmod(self.remaining_seconds, 60)
            self.timer_label.config(text=f"{mins:02}:{secs:02}")
            self.progress['value'] = ((self.total_seconds - self.remaining_seconds) / self.total_seconds) * 100
            self.remaining_seconds -= 1
            time.sleep(1)
            
        if self.is_running:  
            self.timer_label.config(text="🧘 Done!")
            self.status_label.config(text="Meditation complete")
            self.is_running = False
            self.start_button.config(text="Start Meditation", state=tk.NORMAL)
            self.progress['value'] = 100
            
            if self.music_on:
                pygame.mixer.music.stop()
                self.music_on = False
                self.music_button.config(text="🔈 Music: OFF")

if __name__ == "__main__":
    root = tk.Tk()
    app = MeditationApp(root)
    root.mainloop()
