import keyboard
import threading
import time

from vocyn.config import config

class GlobalHotkeyManager:
    def __init__(self, start_callback, stop_callback):
        self.start_callback = start_callback
        self.stop_callback = stop_callback
        self.current_hotkey = config.get("hotkey", "ctrl+alt+space")
        self.is_listening = False
        self.is_holding = False
        
    def _poll_key_release(self):
        """Polls until the key combination is released."""
        # Simple polling, keyboard.is_pressed can check a hotkey combo
        while keyboard.is_pressed(self.current_hotkey):
            time.sleep(0.05)
            
        # Key released
        # print(f"Hotkey {self.current_hotkey} released")
        self.is_holding = False
        self.stop_callback()

    def _on_hotkey(self):
        """Called when the global hotkey is pressed."""
        if not self.is_holding:
            self.is_holding = True
            # print(f"Hotkey {self.current_hotkey} pressed (Holding)")
            self.start_callback()
            
            # Start a thread to watch for the release
            threading.Thread(target=self._poll_key_release, daemon=True).start()
        
    def start(self):
        """Start listening for the globally configured hotkey."""
        if not self.is_listening:
            try:
                keyboard.add_hotkey(self.current_hotkey, self._on_hotkey)
                self.is_listening = True
                # print(f"Started listening for global hotkey: {self.current_hotkey}")
            except Exception as e:
                # print(f"Failed to bind global hotkey {self.current_hotkey}: {e}")
                pass

    def stop(self):
        """Stop listening for the global hotkey."""
        if self.is_listening:
            try:
                keyboard.remove_hotkey(self.current_hotkey)
                self.is_listening = False
                # print(f"Stopped listening for global hotkey: {self.current_hotkey}")
            except Exception as e:
                # Sometimes remove_hotkey fails if it wasn't bound
                # print(f"Error removing global hotkey {self.current_hotkey}: {e}")
                pass
                
    def update_hotkey(self, new_hotkey):
        """Update the global hotkey to listen for."""
        was_listening = self.is_listening
        
        if was_listening:
            self.stop()
            
        self.current_hotkey = new_hotkey
        
        if was_listening:
            self.start()
