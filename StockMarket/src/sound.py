import threading
import time
import os
from src.tts.tts_factory import TTSFactory
from src.logger import Logger
# pip install playsound
from playsound import playsound


class Sound(object):
    AUDIO_SAVE_FILE = os.path.dirname(__file__) + "/../audio.wav"

    def __init__(self):
        self._tts_obj = TTSFactory.create_tts()
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
            Logger.info("播放语音:" + txt)
            is_success, audio_file = self._tts_obj.translate_text(txt)
            if is_success:
                playsound(audio_file, block=True)
                self._wait_read_text = self._wait_read_text[1:]
            else:
                Logger.info("播放语音失败,tts转换语音失败!!!!!!" + txt)

            time.sleep(0.5)

    def add_read_text(self, text):
        if text is None:
            return
        text = text.strip()
        if text == "":
            return
        self._wait_read_text.append(text)


if __name__ == "__main__":
    print(os.path.dirname(__file__))
