#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2021-04-02 16:47:12
# Project: StockMarket

from pyspider.libs.base_handler import *
from src.sound import Sound
from src.logger import Logger
import src.key_word


class Handler(BaseHandler):
    crawl_config = {
        "validate_cert": False,
        # "allow_redirects": False,
        'itag': 'v2',
    }

    def __init__(self):
        self._sound_mgr = Sound()

    @every(minutes=24 * 60)
    def on_start(self):
        Logger.info("开始扫描------------")
        self._sound_mgr.add_read_text(u"开始扫描")
        with open("url.txt") as f:
            for line in f.readlines():
                if line.startswith("#"):
                    continue
                self.crawl(line, callback=self.index_page, age=10 * 60, auto_recrawl=True)
                Logger.info(line)

    @config(age=-1)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        title = response.doc('title').text()
        Logger.info(title)
        if src.key_word.contain_keyword(title):
            self._sound_mgr.add_read_text(title)
        return {
            "url": response.url,
            "title": title,
            'body': response.doc('body').text(),
        }


if __name__ == "__main__":
    Logger.info("test")
    import time
    time.sleep(1)
    pass
