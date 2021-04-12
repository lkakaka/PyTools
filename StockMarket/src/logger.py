import logging
from logging.handlers import TimedRotatingFileHandler
from logging.handlers import RotatingFileHandler
import os
import re

# log_fmt = '%(asctime)s\tFile \"%(filename)s\",line %(lineno)s\t%(levelname)s: %(message)s'
log_fmt = '%(asctime)s %(levelname)s: %(message)s'
formatter = logging.Formatter(log_fmt)
handler = TimedRotatingFileHandler("tmp.log", when="D", interval=1, backupCount=7)
handler.suffix = "%Y-%m-%d_%H-%M.log"
handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}.log$")
handler.setFormatter(formatter)
handler.setLevel(logging.NOTSET)

Logger = logging.getLogger("custom_logger")
Logger.addHandler(handler)
Logger.setLevel(logging.NOTSET)
