
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup


class SpiderBase(object):

    def __init__(self, show_browser):
        self.risk_blocks = {}
        self._wait_time = 1.5
        self._init_driver(show_browser)

    def _init_driver(self, show_browser):
        if show_browser:
            # 创建可见的Chrome浏览器， 方便调试
            self.driver = webdriver.Chrome()
        else:
            # 创建Chrome的无头浏览器
            opt = webdriver.ChromeOptions()
            opt.headless = True
            self.driver = webdriver.Chrome(options=opt)

        self.driver.implicitly_wait(10)

    def sleep(self):
        if self._wait_time <= 0:
            return
        time.sleep(self._wait_time)

    def output_html(self):
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        print(soup.prettify())

    def add_risk_block(self, risk_level, block_name):
        if risk_level == u'低风险地区':
            return
        block_name = block_name.replace(" ", "")
        lst_block = self.risk_blocks.get(risk_level)
        if lst_block is None:
            lst_block = []
            self.risk_blocks[risk_level] = lst_block
        if block_name in lst_block:
            print(u"小区{0}已存在{1}中".format(block_name, risk_level))
            return
        lst_block.append(block_name)

    def output_risk_record(self):
        print("\n\n")
        str_time = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        f_name = u"./RiskBlock_{0}.txt".format(str_time)
        f = open(f_name, 'w', encoding="utf8")
        for risk, blocks in self.risk_blocks.items():
            risk_block_count_str = risk + ":({0}个)".format(len(blocks))
            f.writelines(risk_block_count_str + "\n")
            print(risk_block_count_str)
            for block_name in blocks:
                f.writelines(block_name + "\n")
                print(block_name)
            f.writelines("\n")
            print("\n")
        f.close()
