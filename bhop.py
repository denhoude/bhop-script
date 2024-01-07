import pyautogui
import tkinter as tk
from threading import Thread
import keyboard

class OverlayApp:
    def __init__(self):
        self.is_active = False
        self.auto_press_frequency = 1
        self.start_script_hotkey = 'p'  # Einzelne Taste als Hotkey

        # Tkinter-Fenster erstellen
        self.root = tk.Tk()
        self.root.title("Overlay")
        self.root.geometry("400x200")

        self.label = tk.Label(self.root, text='Status: Press space!')
        self.label.pack(pady=10)

        self.toggle_button = tk.Button(self.root, text="Start/Pause", command=self.toggle_overlay)
        self.toggle_button.pack(pady=10)

        self.settings_button = tk.Button(self.root, text="Open Settings", command=self.open_settings)
        self.settings_button.pack(pady=10)

        self.status_label = tk.Label(self.root, text="")
        self.status_label.pack(pady=10)

        # Tkinter Update
        self.root.after(100, self.update_button_state)
        self.root.after(100, self.check_space_key)

        # Hotkey-Registrierung mit keyboard
        self.register_hotkey()

        # Tkinter-Fenster anzeigen
        self.root.mainloop()

    def register_hotkey(self):
        # Hotkey-Registrierung mit keyboard
        keyboard.unhook_all()
        keyboard.on_press_key(self.start_script_hotkey, self.on_hotkey_pressed)

    def toggle_overlay(self, _=None):
        self.is_active = not self.is_active

    def update_button_state(self):
        if self.is_active:
            self.toggle_button.configure(bg='green')
            self.status_label.configure(text="Status: Active", fg='green')
        else:
            self.toggle_button.configure(bg='red')
            self.status_label.configure(text="Status: Paused", fg='red')

        self.root.after(100, self.update_button_state)

    def check_space_key(self):
        if self.is_active:
            pyautogui.press('space', presses=self.auto_press_frequency)

        self.root.after(100, self.check_space_key)

    def open_settings(self):
        Thread(target=self._open_settings).start()

    def _open_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")

        frequency_label = tk.Label(settings_window, text="Auto-Press Frequency (1-20):")
        frequency_label.pack(pady=5)

        frequency_entry = tk.Entry(settings_window)
        frequency_entry.insert(0, str(self.auto_press_frequency))
        frequency_entry.pack(pady=5)

        hotkey_label = tk.Label(settings_window, text="Hotkey:")
        hotkey_label.pack(pady=5)

        hotkey_entry = tk.Entry(settings_window)
        hotkey_entry.insert(0, str(self.start_script_hotkey))
        hotkey_entry.pack(pady=5)

        save_button = tk.Button(settings_window, text="Save", command=lambda: self.save_settings(settings_window, frequency_entry, hotkey_entry))
        save_button.pack(pady=10)

    def save_settings(self, settings_window, frequency_entry, hotkey_entry):
        try:
            new_frequency = int(frequency_entry.get())
            if 1 <= new_frequency <= 20:
                self.auto_press_frequency = new_frequency
        except ValueError:
            pass

        new_hotkey = hotkey_entry.get()
        if new_hotkey != self.start_script_hotkey:
            self.start_script_hotkey = new_hotkey
            self.register_hotkey()

        # Schließe das Einstellungsfenster
        settings_window.destroy()

    def on_hotkey_pressed(self, e):
        print("Hotkey pressed!")
        self.toggle_overlay()

if __name__ == "__main__":
    app = OverlayApp()
    app.root.mainloop()



