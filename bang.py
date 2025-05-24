import tkinter as tk
from playsound import playsound
import threading
import os # Import os module
import sys # Import sys module

def get_resource_path(relative_path):
    """
    Get the absolute path to a resource, works for dev and for PyInstaller.
    """
    if getattr(sys, 'frozen', False):
        # If the application is frozen (bundled by PyInstaller)
        base_path = sys._MEIPASS
    else:
        # If running as a script (for development)
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def flashbang(duration_time, fade_time=500, sound_file=None):
    root = tk.Tk()
    root.configure(bg='white')
    root.overrideredirect(True)
    root.state('zoomed')

    # Set initial transparency (fully opaque)
    root.attributes('-alpha', 1.0)

    # Play the sound if a sound file is provided
    if sound_file:
        # Use a separate thread to play the sound so it doesn't block the GUI
        threading.Thread(target=playsound, args=(sound_file,)).start()

    # Calculate the number of fade steps and the delay between steps
    num_steps = int(fade_time / 10)
    alpha_decrement = 1.0 / num_steps

    def fade_out():
        current_alpha = root.attributes('-alpha')
        if current_alpha > alpha_decrement:
            root.attributes('-alpha', current_alpha - alpha_decrement)
            root.after(10, fade_out)
        else:
            root.destroy()

    # Start the fade out after the initial flash duration
    root.after(duration_time, fade_out)

    root.mainloop()

def on_key(event):
    if (event.state & 0x4) and event.keysym.lower() == 'f':  # 0x4 is Ctrl
        # Get the correct path to the bundled sound file
        sound_path = get_resource_path('SounD.mp3')
        flashbang(duration_time=999, fade_time=3991, sound_file=sound_path)

if __name__ == "__main__":
    main_app = tk.Tk()
    main_app.title("Press Ctrl+F for Flashbang with Sound")
    main_app.geometry("300x200")
    main_app.bind('<Key>', on_key)
    main_app.mainloop()