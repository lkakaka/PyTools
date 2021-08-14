
from src.logger import Logger
import os


class TTSBase(object):
    WAV_SAVE_FILE = os.path.dirname(__file__) + "/../../audio.wav"
    MP3_SAVE_FILE = os.path.dirname(__file__) + "/../../audio.mp3"

    def translate_text(self, text):
        Logger.error("must implement in drived class")
        return False, None


