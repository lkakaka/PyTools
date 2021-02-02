# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def query():
    import urllib.request
    # req = urllib.request.urlopen('http://bmfw.www.gov.cn/yqfxdjcx/index.html')
    req = urllib.request.urlopen('http://www.gd.gov.cn/gdywdt/zwzt/yqfk/content/post_3021711.html')
    html = req.read().decode('utf-8')
    # print(html)
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.prettify())
    paras_tmp = soup.select('.zw-title') + soup.select('p')
    text = paras_tmp[0:-2]
    print(len(text))
    # print(text)

    datetimes = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    fname = "./" + datetimes + u"Webdata.txt"
    f = open(fname, 'w', encoding="utf8")
    for t in text:
        if len(t) > 0:
            f.writelines(t.get_text() + "\n")
    f.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    query()
    # show_browser = False
    # if len(sys.argv) > 1:
    #     show_browser = True if sys.argv[1] == "1" else False
    # YiQingSpider(show_browser)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
