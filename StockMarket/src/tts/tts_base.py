
from src.logger import Logger


class TTSBase(object):

    def translate_text(self, text, audio_save_file):
        Logger.error("must implement in drived class")


