from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os
from bs4 import BeautifulSoup


class RiskLevel:
    HIGH = 1
    MEDIUM = 2
    LOW = 3

    HIGH_TAG = u"高风险"
    MEDIUM_TAG = u"中风险"
    LOW_TAG = u"低风险"

    HIGH_LV_TEXT = u"高风险区"
    MEDIUM_LV_TEXT = u"中风险区"
    LOW_LV_TEXT = u"低风险区"

    text_2_level = {
        HIGH_TAG: HIGH,
        MEDIUM_TAG: MEDIUM,
        LOW_TAG: LOW,
    }

    level_2_text = {
        HIGH: HIGH_LV_TEXT,
        MEDIUM: MEDIUM_LV_TEXT,
        LOW: LOW_LV_TEXT,
    }

    @staticmethod
    def text_to_risk_level(risk_str):
        for tag, level in RiskLevel.text_2_level.items():
            if risk_str.find(tag) >= 0:
                return level
        raise Exception("unkown risk str:" + risk_str)

    @staticmethod
    def risk_level_to_text(risk_lv):
        return RiskLevel.level_2_text.get(risk_lv)


class SpiderBase(object):

    NEW_ADD_TAG = u"(新增)"

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

    def add_risk_block(self, risk_text, block_name):
        risk_level = RiskLevel.text_to_risk_level(risk_text)
        if risk_level == RiskLevel.LOW:
            return
        block_name = block_name.replace(" ", "")
        lst_block = self.risk_blocks.get(risk_level)
        if lst_block is None:
            lst_block = []
            self.risk_blocks[risk_level] = lst_block
        if block_name in lst_block:
            print(u"小区{0}已存在{1}中".format(block_name, RiskLevel.risk_level_to_text(risk_level)))
            return
        lst_block.append(block_name)

    def output_risk_record(self):
        print("\n\n")
        now_time = time.time()
        last_str_time = time.strftime("%Y-%m-%d", time.localtime(now_time - 3600 * 24))
        last_f_name = u"./RiskBlock_{0}.txt".format(last_str_time)
        last_risk_blocks = None
        if os.path.exists(last_f_name):
            last_risk_blocks = self.read_record_from_file(last_f_name)
        else:
            print("!!!无法输出新增记录,前一天的记录不存在!!!\n")

        str_time = time.strftime("%Y-%m-%d", time.localtime(now_time))
        f_name = u"./RiskBlock_{0}.txt".format(str_time)
        f = open(f_name, 'w', encoding="utf8")
        for risk_lv, blocks in self.risk_blocks.items():
            last_blocks = last_risk_blocks.get(risk_lv) if last_risk_blocks is not None else None
            risk_block_count_str = RiskLevel.risk_level_to_text(risk_lv) + ":({0}个)".format(len(blocks))
            f.writelines(risk_block_count_str + "\n")
            print(risk_block_count_str)
            for block_name in blocks:
                block_str = block_name
                if last_blocks is not None and block_name not in last_blocks:
                    block_str = block_name + SpiderBase.NEW_ADD_TAG
                f.writelines(block_str + "\n")
                print(block_str)
            f.writelines("\n")
            print("\n")
        f.close()

        # self.output_new_add_risk_blocks()

    def read_record_from_file(self, f_name):
        f = open(f_name, 'r', encoding="utf-8")
        risk_blocks = {}
        for line in f.readlines():
            line = line.replace("\n", "")
            if line == "":
                continue
            line = line.replace(SpiderBase.NEW_ADD_TAG, "")
            if line.find(RiskLevel.MEDIUM_TAG) >= 0:
                cur_risk_level = RiskLevel.MEDIUM
                continue
            if line.find(RiskLevel.HIGH_TAG) >= 0:
                cur_risk_level = RiskLevel.HIGH
                continue
            if cur_risk_level not in risk_blocks:
                risk_blocks[cur_risk_level] = []
            risk_blocks[cur_risk_level].append(line)
        f.close()
        return risk_blocks

    # 输出新增区域
    def output_new_add_risk_blocks(self):
        new_risk_blocks = {}
        str_time = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        f_name = u"./RiskBlock_{0}.txt".format(str_time)
        new_f_name = u"./NewRiskBlock_{0}.txt".format(str_time)

        last_str_time = time.strftime("%Y-%m-%d", time.localtime(time.time() - 3600 * 24))
        last_f_name = u"./RiskBlock_{0}.txt".format(last_str_time)

        if not os.path.exists("last_f_name"):
            print("无法输出新增记录,前一天的记录不存在!!!")
            return

        risk_blocks = self.read_record_from_file(f_name)
        last_risk_blocks = self.read_record_from_file(last_f_name)
        new_f = open(new_f_name, 'w', encoding="utf8")

        for risk_lv, risk_blocks in risk_blocks.items():
            last_blocks = last_risk_blocks.get(risk_lv)
            for risk_block in risk_blocks:
                if last_blocks is None or risk_block not in last_blocks:
                    if risk_lv not in new_risk_blocks:
                        new_risk_blocks[risk_lv] = []
                    new_risk_blocks[risk_lv].append(risk_block)
        for risk_lv, blocks in new_risk_blocks.items():
            new_risk_info = "新增{0}{1}个".format(RiskLevel.risk_level_to_text(risk_lv), len(blocks))
            print(new_risk_info)
            new_f.writelines(new_risk_info)
            for block in blocks:
                print(block)
                new_f.writelines(block)
        new_f.close()

