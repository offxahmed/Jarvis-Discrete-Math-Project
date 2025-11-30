import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageSequence
import json
import threading
import time
from backend.speech_to_text import listen
from backend.text_to_speech import speak
from backend.model import decide_query_type
from main import jarvis_brain

class JarvisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("J.A.R.V.I.S")
        self.root.geometry("1200x700")
        self.root.configure(bg="#0a0e27")
        
        # Remove window border for futuristic look
        self.root.overrideredirect(True)
        
        # Load status
        self.is_listening = False
        self.is_speaking = False
        
        # Create UI
        self.create_widgets()
        
        # Start animation thread
        self.animation_thread = threading.Thread(target=self.animate_jarvis, daemon=True)
        self.animation_thread.start()
        
    def create_widgets(self):
        """Create all GUI elements"""
        
        # Top bar with controls
        top_bar = tk.Frame(self.root, bg="#1a1f3a", height=50)
        top_bar.pack(fill=tk.X)
        
        # Title
        title_label = tk.Label(top_bar, text="J.A.R.V.I.S", 
                              font=("Arial", 20, "bold"), 
                              fg="#00d4ff", bg="#1a1f3a")
        title_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Control buttons
        self.minimize_btn = tk.Button(top_bar, text="─", 
                                     command=self.minimize_window,
                                     bg="#1a1f3a", fg="white", 
                                     font=("Arial", 16), bd=0)
        self.minimize_btn.pack(side=tk.RIGHT, padx=5)
        
        self.close_btn = tk.Button(top_bar, text="✕", 
                                   command=self.root.quit,
                                   bg="#1a1f3a", fg="#ff4444", 
                                   font=("Arial", 16), bd=0)
        self.close_btn.pack(side=tk.RIGHT, padx=5)
        
        # Main content area
        content_frame = tk.Frame(self.root, bg="#0a0e27")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Jarvis animation (center)
        self.animation_label = tk.Label(content_frame, bg="#0a0e27")
        self.animation_label.pack(pady=30)
        
        # Status text
        self.status_label = tk.Label(content_frame, 
                                     text="Initializing...", 
                                     font=("Arial", 16), 
                                     fg="#00d4ff", bg="#0a0e27")
        self.status_label.pack(pady=10)
        
        # Response display
        self.response_text = tk.Text(content_frame, 
                                    height=8, width=70,
                                    font=("Arial", 12),
                                    bg="#1a1f3a", fg="#00ff88",
                                    bd=0, wrap=tk.WORD)
        self.response_text.pack(pady=20)
        
        # Microphone button
        self.mic_button = tk.Button(content_frame, 
                                    text="🎤 Click to Speak",
                                    command=self.toggle_listening,
                                    font=("Arial", 14),
                                    bg="#00d4ff", fg="black",
                                    padx=30, pady=10,
                                    cursor="hand2")
        self.mic_button.pack(pady=20)
        
    def animate_jarvis(self):
        """Animate the Jarvis GIF"""
        try:
            gif_path = "frontend/graphics/Jarvis.gif"
            gif = Image.open(gif_path)
            frames = [ImageTk.PhotoImage(frame.copy().resize((300, 300))) 
                     for frame in ImageSequence.Iterator(gif)]
            
            frame_index = 0
            while True:
                if not self.is_speaking:
                    self.animation_label.configure(image=frames[frame_index])
                    frame_index = (frame_index + 1) % len(frames)
                
                time.sleep(0.05)  # 50ms per frame
                
        except Exception as e:
            print(f"Animation error: {e}")
    
    def toggle_listening(self):
        """Start/stop listening"""
        if not self.is_listening:
            self.is_listening = True
            self.status_label.config(text="Listening...")
            self.mic_button.config(bg="#ff4444", text="🎤 Listening...")
            
            # Start listening thread
            listen_thread = threading.Thread(target=self.process_voice_command, daemon=True)
            listen_thread.start()
        else:
            self.is_listening = False
            self.status_label.config(text="Ready")
            self.mic_button.config(bg="#00d4ff", text="🎤 Click to Speak")
    
    def process_voice_command(self):
        """Listen and process voice input"""
        query = listen()
        
        if query:
            self.response_text.delete(1.0, tk.END)
            self.response_text.insert(tk.END, f"You: {query}\n\n")
            
            self.status_label.config(text="Processing...")
            
            # Get response from Jarvis brain
            response = jarvis_brain(query)
            
            self.response_text.insert(tk.END, f"Jarvis: {response}")
            
            # Speak response
            self.is_speaking = True
            self.status_label.config(text="Speaking...")
            speak(response)
            self.is_speaking = False
            
        self.is_listening = False
        self.status_label.config(text="Ready")
        self.mic_button.config(bg="#00d4ff", text="🎤 Click to Speak")
    
    def minimize_window(self):
        """Minimize window"""
        self.root.iconify()
    
    def update_status_from_file(self):
        """Read status.json and update UI"""
        try:
            with open("frontend/files/status.json", "r") as f:
                status = json.load(f)
                self.status_label.config(text=status.get("current_status", "Ready"))
        except:
            pass

def run_gui():
    """Launch the GUI"""
    root = tk.Tk()
    app = JarvisGUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui()
