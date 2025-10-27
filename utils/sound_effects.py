"""
Sound Effects Module
Provides audio feedback using winsound (Windows built-in library)
Handles correct/wrong answers, achievements, and other game events
"""

import winsound
import threading


class SoundManager:
    """Manages all sound effects for the quiz application"""
    
    def __init__(self):
        self.enabled = True
    
    def enable(self):
        """Enable sound effects"""
        self.enabled = True
    
    def disable(self):
        """Disable sound effects"""
        self.enabled = False
    
    def play_in_thread(self, frequency, duration):
        """Play sound in separate thread to avoid blocking UI"""
        if not self.enabled:
            return
        
        def play():
            try:
                winsound.Beep(frequency, duration)
            except:
                pass  # Silently fail if sound cannot be played
        
        thread = threading.Thread(target=play, daemon=True)
        thread.start()
    
    def play_correct(self):
        """Play sound for correct answer"""
        self.play_in_thread(800, 200)  # High pleasant tone
    
    def play_wrong(self):
        """Play sound for wrong answer"""
        self.play_in_thread(300, 300)  # Low error tone
    
    def play_achievement(self):
        """Play sound for achievement unlocked"""
        if not self.enabled:
            return
        # Play ascending tones for achievement
        def play_sequence():
            try:
                winsound.Beep(523, 150)  # C5
                winsound.Beep(659, 150)  # E5
                winsound.Beep(784, 200)  # G5
            except:
                pass
        
        thread = threading.Thread(target=play_sequence, daemon=True)
        thread.start()
    
    def play_level_up(self):
        """Play sound for level up or milestone"""
        if not self.enabled:
            return
        def play_sequence():
            try:
                winsound.Beep(440, 150)  # A4
                winsound.Beep(523, 150)  # C5
                winsound.Beep(659, 150)  # E5
                winsound.Beep(880, 250)  # A5
            except:
                pass
        
        thread = threading.Thread(target=play_sequence, daemon=True)
        thread.start()
    
    def play_perfect_score(self):
        """Play special sound for perfect score"""
        if not self.enabled:
            return
        def play_sequence():
            try:
                # Triumphant fanfare
                winsound.Beep(523, 100)
                winsound.Beep(659, 100)
                winsound.Beep(784, 100)
                winsound.Beep(1047, 300)
            except:
                pass
        
        thread = threading.Thread(target=play_sequence, daemon=True)
        thread.start()
    
    def play_streak(self):
        """Play sound for streak milestone"""
        if not self.enabled:
            return
        def play_sequence():
            try:
                winsound.Beep(700, 150)
                winsound.Beep(900, 150)
            except:
                pass
        
        thread = threading.Thread(target=play_sequence, daemon=True)
        thread.start()
    
    def play_time_warning(self):
        """Play warning sound when time is running out"""
        self.play_in_thread(600, 100)
    
    def play_time_expired(self):
        """Play sound when time expires"""
        if not self.enabled:
            return
        def play_sequence():
            try:
                winsound.Beep(400, 150)
                winsound.Beep(350, 150)
                winsound.Beep(300, 200)
            except:
                pass
        
        thread = threading.Thread(target=play_sequence, daemon=True)
        thread.start()


# Global sound manager instance
sound_manager = SoundManager()
