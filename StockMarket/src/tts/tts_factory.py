import src.config
from src.tts.aly_tts import AlyTTS
from src.tts.g_tts import GTTS


class TTSFactory(object):
    ALL_TTS = {
        "aly": AlyTTS,
        "google": GTTS,
    }

    @staticmethod
    def create_tts():
        tts = src.config.Config.get_config_str("tts")
        print("select tts:" + tts)
        tts_cls = TTSFactory.ALL_TTS.get(tts, AlyTTS)
        return tts_cls()


if __name__ == "__main__":
    tts = TTSFactory.create_tts()
    is_success, audio_file = tts.translate_text("这是什么东西")
    from playsound import playsound
    playsound(audio_file, block=True)

