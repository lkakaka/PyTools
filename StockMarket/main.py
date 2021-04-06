#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2021-04-02 16:47:12
# Project: StockMarket

from pyspider.libs.base_handler import *
from aly_tts import AlyTTS
import threading
import time

import logging

LOG_FILE = "./log.txt"
with open(LOG_FILE, mode='w', encoding='utf-8') as ff:
    print("create log file")

_logger = logging.getLogger()
handler = logging.FileHandler(LOG_FILE)
_logger.addHandler(handler)
_logger.setLevel(logging.NOTSET)


class Handler(BaseHandler):
    crawl_config = {
    }

    wait_read_text = []

    @every(minutes=24 * 60)
    def on_start(self):
        _logger.info("start crawl------------")
        self.crawl('http://www.zgjrj.com/gushi/', allow_redirects=False, callback=self.index_page)
        Handler.wait_read_text.append(u"开始扫描")
        Handler.wait_read_text.append(u"你好")
        t1 = threading.Thread(target=self.play_sound_thread_func)
        t1.start()

    @config(age=10)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        Handler.wait_read_text.append(response.doc('title').text());
        return {
            "url": response.url,
            "title": response.doc('title').text(),
            'p': response.doc('p').text(),
        }

    def play_sound_thread_func(self):
        while True:
            if len(Handler.wait_read_text) == 0:
                # _logger.info("play_sound_thread_func sleep------------")
                time.sleep(1)
                continue
            txt = Handler.wait_read_text[0]
            Handler.wait_read_text = Handler.wait_read_text[1:]
            _logger.info("play sound start------------" + txt)
            AlyTTS.read_text(txt)
            _logger.info("play sound start------------")


if __name__ == "__main__":
    pass
    # handler = Handler()
    # handler.on_start()
    # import logging
    #
    # LOG_FILE = "./log.txt"
    # with open(LOG_FILE, mode='w', encoding='utf-8') as ff:
    #     print("create log file")
    #
    # logger = logging.getLogger()
    # handler = logging.FileHandler(LOG_FILE)
    # logger.addHandler(handler)
    # logger.setLevel(logging.NOTSET)
    #
    # logger.info("test----------")
