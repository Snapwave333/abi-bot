import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import subprocess
import sys
import os
import threading
import time
from dotenv import load_dotenv

# Global lock to prevent simultaneous syncs settings
sync_lock = threading.Lock()
stop_event = threading.Event()

def get_interval():
    """Load interval from .env, default to 24 hours."""
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    # Reload env file manually to get fresh values
    vals = {}
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    vals[k] = v
    
    try:
        return float(vals.get("SYNC_INTERVAL_HOURS", 24))
    except:
        return 24.0

def run_sync_process(icon=None):
    """Runs the sync process safely."""
    if sync_lock.acquire(blocking=False):
        try:
            if icon:
                icon.notify("Starting Sync...", "ABI Bot")
            
            # Run main.py
            subprocess.run(
                [sys.executable, "main.py"],
                cwd=os.path.dirname(os.path.abspath(__file__)),
                creationflags=subprocess.CREATE_NO_WINDOW # Run mostly silent for background
            )
            
            if icon:
                icon.notify("Sync Complete!", "ABI Bot")
                
        except Exception as e:
            if icon:
                icon.notify(f"Sync Failed: {e}", "Error")
        finally:
            sync_lock.release()
    else:
        if icon:
            icon.notify("Sync already in progress.", "ABI Bot")

def scheduler_loop(icon):
    """Background loop to run sync at intervals."""
    last_run = 0
    
    while not stop_event.is_set():
        interval_hours = get_interval()
        interval_seconds = interval_hours * 3600
        
        now = time.time()
        
        # If never run, or time elapsed
        if (now - last_run) > interval_seconds:
            # We delay the VERY first run slightly to let system startup finish if needed, 
            # but user wants "forever start at system startup", implying active usage.
            # Let's run.
            print(f"Auto-sync triggering. Interval: {interval_hours}h")
            run_sync_process(icon) # Optional: Don't notify on auto-runs to avoid spam? 
            # User might want to know. Let's keep notifications for now or simple log.
            # actually run_sync_process sends notifications.
            
            last_run = time.time()
        
        # Check every minute
        time.sleep(60)

def create_image(width, height, color1, color2):
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)
    return image

def on_sync(icon, item):
    # Run in thread so we don't block the UI loop for the few seconds checks take
    threading.Thread(target=run_sync_process, args=(icon,)).start()

def on_settings(icon, item):
    try:
        subprocess.Popen(
            [sys.executable, "settings_ui.py"],
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
    except Exception as e:
        icon.notify(f"Failed to launch settings: {e}", "Error")

def on_exit(icon, item):
    stop_event.set()
    icon.stop()

def setup(icon):
    icon.visible = True
    # Start scheduler thread
    t = threading.Thread(target=scheduler_loop, args=(icon,), daemon=True)
    t.start()

def main():
    image = create_image(64, 64, 'black', 'orange')
    
    menu = (
        item('Sync Now', on_sync),
        item('Settings', on_settings, default=True),
        item('Exit', on_exit)
    )

    icon = pystray.Icon("name", image, "ABI Bot\nRight-click for menu\nDouble-click for Settings", menu)
    icon.run(setup)

if __name__ == "__main__":
    main()
