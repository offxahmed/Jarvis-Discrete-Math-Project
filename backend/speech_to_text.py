import whisper
import speech_recognition as sr
from dotenv import load_dotenv
import os
import tempfile

load_dotenv()

# Load Whisper model (use 'base' for speed, 'medium' for accuracy)
model = whisper.load_model("base")

# Create temp audio file path in the current directory
TEMP_AUDIO_PATH = os.path.join(os.getcwd(), "temp_audio.wav")

# Check for FFmpeg availability
import shutil
FFMPEG_AVAILABLE = shutil.which("ffmpeg") is not None

def listen():
    """Capture audio and convert to text using Whisper (with fallback)"""
    # If FFmpeg is missing, use Google SR immediately
    if not FFMPEG_AVAILABLE:
        print("Warning: FFmpeg not found using Google Speech Recognition as fallback.")
        return listen_google()

    recognizer = sr.Recognizer()
    
    try:
        # List available microphones
        mic_list = sr.Microphone.list_microphone_names()
        if not mic_list:
            print("Error: No microphone detected!")
            return None
        
        # Use default microphone
        with sr.Microphone() as source:
            print("Listening...")
            # Adjust for ambient noise with shorter duration
            recognizer.adjust_for_ambient_noise(source, duration=0.3)
            recognizer.energy_threshold = 4000  # Increase sensitivity
            
            try:
                # Listen for audio with timeout
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                # Save audio temporarily with absolute path
                with open(TEMP_AUDIO_PATH, "wb") as f:
                    f.write(audio.get_wav_data())
                
                # Transcribe with Whisper
                result = model.transcribe(TEMP_AUDIO_PATH, language=os.getenv("INPUT_LANGUAGE", "en"))
                
                query = result["text"].strip()
                if query:
                    print(f"You said: {query}")
                    return query
                else:
                    return None
            
            except FileNotFoundError:
                # Catch [WinError 2] specifically for missing ffmpeg during execution
                print("Error: FFmpeg not found processing audio. Falling back to Google.")
                return listen_google()
            except sr.WaitTimeoutError:
                print("No speech detected, listening again...")
                return None
            except Exception as e:
                # Fallback to Google if Whisper fails for other reasons
                print(f"Error during transcription: {e}. Falling back to Google.")
                return listen_google()
                
    except Exception as e:
        print(f"Microphone error: {e}")
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
