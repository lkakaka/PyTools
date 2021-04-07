
import threading
import time
import os
from src.tts.aly_tts import AlyTTS
from src.logger import Logger
# pip install playsound
from playsound import playsound


class Sound(object):

    AUDIO_SAVE_FILE = os.path.dirname(__file__) + "/../audio.wav"

    def __init__(self):
        self._tts_obj = AlyTTS()
        self._wait_read_text = []
        self._sound_thread = threading.Thread(target=self.play_sound_thread_func)
        self._sound_thread.start()

    def play_sound_thread_func(self):
        while True:
            if len(self._wait_read_text) == 0:
                # _logger.info("play_sound_thread_func sleep------------")
                time.sleep(1)
                continue
            txt = self._wait_read_text[0]
            self._wait_read_text = self._wait_read_text[1:]
            Logger.info("play sound start------------" + txt)
            self._tts_obj.translate_text(txt, Sound.AUDIO_SAVE_FILE)
            playsound(Sound.AUDIO_SAVE_FILE, block=True)
            Logger.info("play sound end------------")
            time.sleep(0.5)

    def add_read_text(self, text):
        self._wait_read_text.append(text)


if __name__ == "__main__":
    print(os.path.dirname(__file__))