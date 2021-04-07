

import logging

LOG_FILE = "../log.txt"
with open(LOG_FILE, mode='w', encoding='utf-8') as ff:
    print("create log file")

Logger = logging.getLogger()
handler = logging.FileHandler(LOG_FILE)
Logger.addHandler(handler)
Logger.setLevel(logging.NOTSET)

