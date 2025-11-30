import whisper
import speech_recognition as sr
from dotenv import load_dotenv
import os

load_dotenv()

# Load Whisper model (use 'base' for speed, 'medium' for accuracy)
model = whisper.load_model("base")

def listen():
    """Capture audio and convert to text using Whisper"""
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            # Save audio temporarily
            with open("temp_audio.wav", "wb") as f:
                f.write(audio.get_wav_data())
            
            # Transcribe with Whisper
            result = model.transcribe("temp_audio.wav", language=os.getenv("INPUT_LANGUAGE", "en"))
            
            query = result["text"]
            print(f"You said: {query}")
            return query
            
        except sr.WaitTimeoutError:
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

# Alternative: Google Speech Recognition for faster response
def listen_google():
    """Fallback method using Google SR"""
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        
        try:
            query = recognizer.recognize_google(audio, language=os.getenv("INPUT_LANGUAGE", "en-US"))
            return query
        except:
            return None
