# -*- coding: UTF-8 -*-

# pip install gTTS
from gtts import gTTS
from src.tts.tts_base import TTSBase

LANG_ZH = "zh"  # 中文
LANG_ZH_TW = "zh-TW"  # 中文（台湾)
LANG_JAPANESE = "ja"  # 日语
LANG_ENGLISH = "en"  # 英语


class GTTS(TTSBase):

    def __init__(self):
        pass

    def translate_text(self, text):
        audio_file = TTSBase.MP3_SAVE_FILE
        gtts = gTTS(text, lang=LANG_ZH)
        gtts.save(audio_file)
        return True, audio_file


if __name__ == "__main__":
    audio_file = TTSBase.MP3_SAVE_FILE
    tts = gTTS("这是什么东西", lang=LANG_ZH, slow=True)
    tts.save(audio_file)
    from playsound import playsound

    playsound(audio_file, block=True)

    tts = gTTS("これは何ですか", lang=LANG_JAPANESE, slow=True)
    tts.save(audio_file)
    playsound(audio_file, block=True)

    tts = gTTS("What's this?", lang=LANG_ENGLISH, slow=True)
    tts.save(audio_file)
    playsound(audio_file, block=True)
