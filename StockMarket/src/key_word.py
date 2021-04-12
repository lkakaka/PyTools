import os
from src.logger import Logger

KEY_WORDS = []
KEYWORD_FILE = os.path.dirname(__file__) + "/../keyword.txt"
with open(KEYWORD_FILE) as f:
    for line in f.readlines():
        line = line.strip()
        if line.startswith("#"):
            continue
        KEY_WORDS.append(line)

Logger.info("关键词:\n" + "\n".join(KEY_WORDS))


def contain_keyword(text):
    for key_word in KEY_WORDS:
        if text.find(key_word) >= 0:
            return True
    return False
