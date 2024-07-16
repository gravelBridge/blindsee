import pyttsx3
from ..config.config import Config
from ..utils.logger import Logger

class TextToSpeech:
    """
    Handles text-to-speech functionality.
    Uses pyttsx3 for offline TTS on the Raspberry Pi.
    If pyttsx3 initialization fails, tries a fallback (if any).

    Methods:
        speak(text: str):
            Speaks the given text.
    """

    def __init__(self):
        self.logger = Logger("TTS")
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', Config.VOICE_RATE)
            self.engine.setProperty('volume', Config.VOICE_VOLUME)
            # On some systems, you can choose voices:
            # voices = self.engine.getProperty('voices')
            # self.engine.setProperty('voice', voices[0].id)  # pick a voice
            self.logger.info("TTS engine initialized successfully.")
        except Exception as e:
            self.logger.error(f"Failed to initialize TTS engine: {e}")
            self.engine = None

    def speak(self, text: str):
        """
        Speaks the given text aloud using TTS.
        Logs an error if TTS engine is not available.
        """
        if not self.engine:
            self.logger.error("TTS engine not available. Cannot speak.")
            return
        if not text or not text.strip():
            self.logger.warn("Empty text provided to speak, skipping.")
            return

        self.logger.debug(f"Speaking: {text}")
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            self.logger.error(f"Error during TTS: {e}")
