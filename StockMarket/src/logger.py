import logging
import os

LOG_FILE = os.path.dirname(__file__) + "/../log.txt"
with open(LOG_FILE, mode='w', encoding='utf-8') as ff:
    print("create log file:" + LOG_FILE)

Logger = logging.getLogger()
handler = logging.FileHandler(LOG_FILE)
Logger.addHandler(handler)
Logger.setLevel(logging.NOTSET)
