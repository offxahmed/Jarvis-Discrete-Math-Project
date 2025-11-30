import pyautogui
import subprocess
import os
import webbrowser
import pywhatkit
import psutil
from datetime import datetime

def open_application(app_name):
    """Open applications by name"""
    apps = {
        "notepad": "notepad.exe",
        "chrome": "chrome.exe",
        "firefox": "firefox.exe",
        "spotify": "spotify.exe",
        "vscode": "code",
        "calculator": "calc.exe",
        "cmd": "cmd.exe",
        "terminal": "cmd.exe"
    }
    
    app_name = app_name.lower()
    
    try:
        if app_name in apps:
            subprocess.Popen(apps[app_name])
            return f"Opening {app_name}"
        else:
            # Try opening as is
            os.startfile(app_name)
            return f"Opening {app_name}"
    except Exception as e:
        return f"Couldn't open {app_name}: {str(e)}"

def close_application(app_name):
    """Close running applications"""
    try:
        for proc in psutil.process_iter(['name']):
            if app_name.lower() in proc.info['name'].lower():
                proc.kill()
                return f"Closed {app_name}"
        return f"{app_name} is not running"
    except Exception as e:
        return f"Error closing {app_name}: {str(e)}"

def open_website(url):
    """Open websites in browser"""
    if not url.startswith('http'):
        url = 'https://' + url
    
    webbrowser.open(url)
    return f"Opening {url}"

def youtube_search(query):
    """Search and play on YouTube"""
    pywhatkit.playonyt(query)
    return f"Playing {query} on YouTube"

def system_control(command):
    """Control system functions"""
    command = command.lower()
    
    if "mute" in command or "unmute" in command:
        pyautogui.press("volumemute")
        return "Volume muted/unmuted"
    
    elif "volume up" in command or "increase volume" in command:
        for _ in range(5):
            pyautogui.press("volumeup")
        return "Volume increased"
    
    elif "volume down" in command or "decrease volume" in command:
        for _ in range(5):
            pyautogui.press("volumedown")
        return "Volume decreased"
    
    elif "screenshot" in command:
        screenshot = pyautogui.screenshot()
        filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        screenshot.save(filename)
        return f"Screenshot saved as {filename}"
    
    elif "lock" in command:
        os.system("rundll32.user32.dll,LockWorkStation")
        return "Locking computer"
    
    elif "shutdown" in command:
        os.system("shutdown /s /t 1")
        return "Shutting down"
    
    elif "restart" in command:
        os.system("shutdown /r /t 1")
        return "Restarting"
    
    else:
        return "System command not recognized"

def open_multiple_tabs(queries):
    """Open multiple browser tabs simultaneously"""
    for query in queries:
        webbrowser.open_new_tab(query)
    return f"Opened {len(queries)} tabs"
