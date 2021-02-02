from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os
from bs4 import BeautifulSoup
from docx import Document
import datetime
import re


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


class RiskBlock:

    def __init__(self, province, block):
        self.province = province
        self.block = block
        self.is_new_add = False

    @property
    def full_name(self):
        return self.province + self.block

    def full_name_with_sep(self):
        return self.province + " " + self.block

    def full_name_with_new_tag(self):
        new_tag = SpiderBase.NEW_ADD_TAG if self.is_new_add else ""
        return "{0}{1}{2}".format(self.province, self.block, new_tag)

    def block_name_with_new_tag(self):
        new_tag = SpiderBase.NEW_ADD_TAG if self.is_new_add else ""
        return "{0}{1}".format(self.block, new_tag)

    def __eq__(self, other):
        return self.province == other.province and self.block == other.block


class SpiderBase(object):

    NEW_ADD_TAG = u"(新增)"
    OUTPUT_PATH = "../"
    TEMP_PATH = "../tmp/"

    def __init__(self, show_browser):
        self.risk_blocks = {RiskLevel.HIGH: [], RiskLevel.MEDIUM: []}
        self.last_blocks = None
        self.result_time = None
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
        block_lst = block_name.split(" ")
        risk_block = RiskBlock(block_lst[0], "".join(block_lst[1:]))
        # block_name = block_name.replace(" ", "")
        lst_block = self.risk_blocks.get(risk_level)
        if risk_block in lst_block:
            print(u"小区{0}已存在{1}中".format(block_name, RiskLevel.risk_level_to_text(risk_level)))
            return
        lst_block.append(risk_block)

    def output_risk_record(self):
        print("\n\n")
        now_time = time.time()
        last_str_time = time.strftime("%Y-%m-%d", time.localtime(now_time - 3600 * 24))
        # last_f_name = u"{0}RiskBlock_{1}.txt".format(SpiderBase.TEMP_PATH, last_str_time)
        last_result_time_tup = time.localtime(now_time - 3600 * 24)
        last_result_time_str = u"{0}月{1}日15时".format(last_result_time_tup.tm_mon, last_result_time_tup.tm_mday)
        last_f_name = u"{0}关于发布国内疫情风险等级提示的通知（截至{1}）.docx".format(SpiderBase.OUTPUT_PATH, last_result_time_str)
        if os.path.exists(last_f_name):
            # self.last_blocks = self.read_record_from_file(last_f_name)
            self.last_blocks = self.read_record_from_word(last_f_name)
        else:
            print("!!!无法输出新增记录,前一天的记录不存在!!!{0}\n".format(last_f_name))

        str_time = time.strftime("%Y-%m-%d", time.localtime(now_time))
        f_name = u"{0}RiskBlock_{1}.txt".format(SpiderBase.TEMP_PATH, str_time)
        f = open(f_name, 'w', encoding="utf8")
        medium_risk_block = {}  # {province : [RiskBlock,]}
        for risk_lv, blocks in self.risk_blocks.items():
            risk_block_count_str = RiskLevel.risk_level_to_text(risk_lv) + ":({0}个)".format(len(blocks))
            f.writelines(risk_block_count_str + "\n")
            print(risk_block_count_str)
            for block in blocks:
                block_str = block.full_name_with_sep()
                if self.last_blocks is not None and block not in self.last_blocks[RiskLevel.HIGH] and block not in self.last_blocks[RiskLevel.MEDIUM]:
                    block.is_new_add = True
                    block_str = block_str + SpiderBase.NEW_ADD_TAG
                f.writelines(block_str + "\n")
                print(block_str)

                if risk_lv == RiskLevel.MEDIUM:
                    if block.province not in medium_risk_block:
                        medium_risk_block[block.province] = []
                    medium_risk_block[block.province].append(block)

            f.writelines("\n")
            print("\n")
        f.close()

        new_blocks = self.calc_new_block()
        new_high_block_str = ""
        new_medium_block_str = ""
        new_low_block_str = ""
        if new_blocks is not None:
            new_high_block_str = self.join_block(u"、", new_blocks.get(RiskLevel.HIGH))
            new_medium_block_str = self.join_block(u"、", new_blocks.get(RiskLevel.MEDIUM))
            new_low_block_str = self.join_block(u"、", new_blocks.get(RiskLevel.LOW))

        high_risk_str = ""
        high_risk_blocks = self.risk_blocks[RiskLevel.HIGH]
        for block in high_risk_blocks:
            high_risk_str += "{0}\n".format(block.full_name)

        med_risk_str = ""
        medium_block_idx = 1
        for prov, blocks in medium_risk_block.items():
            med_risk_str += u"{0}（共{1}个）\n".format(prov, len(blocks))
            for block in blocks:
                med_risk_str += "{0}.{1}\n".format(medium_block_idx, block.block_name_with_new_tag())
                medium_block_idx += 1
            med_risk_str += "\n"

        result_time_tup = self.result_time.timetuple()
        result_time_str = u"{0}月{1}日{2}时".format(result_time_tup.tm_mon, result_time_tup.tm_mday, result_time_tup.tm_hour)
        # result_time_str = self.result_time.strftime("%m月%d日%H时")
        cur_time_tup = datetime.datetime.now().timetuple()
        cur_date_str = u"{0}年{1}月{2}日".format(cur_time_tup.tm_year, cur_time_tup.tm_mon, cur_time_tup.tm_mday)
        # cur_date_str = time.strftime("%Y年%m月%d日", time.localtime(now_time))

        doc = Document(u'{0}模板.docx'.format(SpiderBase.OUTPUT_PATH))
        paragraphs = doc.paragraphs
        for par in paragraphs:
            for run in par.runs:
                run.text = run.text.replace("ResultTime", result_time_str)
                run.text = run.text.replace("NewHighRiskBlock", new_high_block_str)
                run.text = run.text.replace("NewMediumRiskBlock", new_medium_block_str)
                run.text = run.text.replace("CurDate", cur_date_str)
                run.text = run.text.replace("NewLowRiskBlock", new_low_block_str)
                run.text = run.text.replace("HighRiskBlockCount", str(len(high_risk_blocks)))
                run.text = run.text.replace("HighRiskBlockContent", high_risk_str)
                run.text = run.text.replace("MediumRiskBlockCount", str(medium_block_idx - 1))
                run.text = run.text.replace("MediumRiskBlockContent", med_risk_str)
                # if run.text.find("MediumRiskBlockContent") >= 0:
                #     run.text = run.text.replace("MediumRiskBlockContent", "")
                #     medium_block_idx = 1
                #     style = run.style
                #     for prov, blocks in medium_risk_block.items():
                #         med_risk_str = u"{0}（共{1}个）\n".format(prov, len(blocks))
                #         new_run = par.add_run(med_risk_str, style)
                #         new_run.add_break()
                #         for block in blocks:
                #             med_risk_str = "{0}.{1}\n".format(medium_block_idx, block.block_name_with_new_tag())
                #             new_run = par.add_run(med_risk_str, style)
                #             new_run.add_break()
                #             medium_block_idx += 1

        save_file_name = u"{0}关于发布国内疫情风险等级提示的通知（截至{1}）.docx".format(SpiderBase.OUTPUT_PATH, result_time_str)
        doc.save(save_file_name)
        # self.output_new_add_risk_blocks()

    def join_block(self, sep, blocks):
        block_str = ""
        count = len(blocks)
        for i in range(count):
            block_str += blocks[i].full_name
            if i != count - 1:
                block_str += sep
        return block_str

    # 计算调整的地区
    def calc_new_block(self):
        if self.last_blocks is None:
            return
        high_block = self.risk_blocks[RiskLevel.HIGH]
        medium_block = self.risk_blocks[RiskLevel.MEDIUM]
        last_high_block = self.last_blocks.get(RiskLevel.HIGH)
        last_medium_block = self.last_blocks.get(RiskLevel.MEDIUM)

        new_high_block = []
        new_medium_block = []
        new_low_block = []
        for block in high_block:
            if block in last_high_block:
                continue
            new_high_block.append(block)

        for block in medium_block:
            if block in last_medium_block:
                continue
            new_medium_block.append(block)

        for block in last_high_block:
            if block in high_block:
                continue
            if block in medium_block:
                new_medium_block.append(block)
                continue
            new_low_block.append(block)

        for block in last_medium_block:
            if block in medium_block:
                continue
            if block in high_block:
                new_high_block.append(block)
                continue
            new_low_block.append(block)

        return {RiskLevel.HIGH: new_high_block, RiskLevel.MEDIUM: new_medium_block, RiskLevel.LOW: new_low_block}

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
            block_lst = line.split(" ")
            risk_block = RiskBlock(block_lst[0], "".join(block_lst[1:]))

            risk_blocks[cur_risk_level].append(risk_block)
        f.close()
        return risk_blocks

    @staticmethod
    def read_record_from_word(f_name):
        risk_blocks = {RiskLevel.HIGH: [], RiskLevel.MEDIUM: []}
        doc = Document(f_name)
        paragraphs = doc.paragraphs
        # pars_string = [par.text for par in paragraphs]
        # print(pars_string)
        is_start = False
        h_start_idx = 0
        h_end_idx = 0
        m_start_idx = 0

        for idx in range(len(paragraphs)):
            par = paragraphs[idx]
            idx += 1
            # print(par.text)
            if par.text == "":
                continue
            if par.text.find(u"国内疫情中高风险地区列表") >= 0:
                is_start = True
                continue
            if not is_start:
                continue
            if par.text.find(u"高风险地区") >= 0:
                h_start_idx = idx
                continue
            if par.text.find(u"中风险地区") >= 0:
                m_start_idx = idx
                h_end_idx = idx - 2
                continue

        for h_idx in range(h_start_idx, h_end_idx + 1):
            h_par = paragraphs[h_idx]
            h_text = h_par.text.replace(SpiderBase.NEW_ADD_TAG, "")
            for text in h_text.split("\n"):
                prov_pos = text.find(u"省")
                if prov_pos < 0:
                    prov_pos = text.find(u"市")
                if prov_pos < 0:
                    continue
                province = text[0:prov_pos+1]
                block = text[prov_pos+1:]
                # print(province, block)
                risk_block = RiskBlock(province, block)
                risk_blocks[RiskLevel.HIGH].append(risk_block)

        for m_idx in range(m_start_idx, len(paragraphs)):
            m_par = paragraphs[m_idx]
            m_text = m_par.text.replace(SpiderBase.NEW_ADD_TAG, "")
            for text in m_text.split("\n"):
                if not re.match(r"^\d.*", text):
                    prov_pos = text.find(u"省")
                    if prov_pos < 0:
                        prov_pos = text.find(u"市")
                    if prov_pos < 0:
                        continue
                    m_province = text[0:prov_pos + 1]
                else:
                    dot_pos = text.find(u".")
                    if dot_pos >= 0:
                        block_name = text[dot_pos+1:]
                        risk_block = RiskBlock(m_province, block_name)
                        risk_blocks[RiskLevel.MEDIUM].append(risk_block)
                        # print(m_province, block_name)

        print("昨日高风险:{0}, 中风险:{1}".format(len(risk_blocks[RiskLevel.HIGH]), len(risk_blocks[RiskLevel.MEDIUM])))
        return risk_blocks


    # 输出新增区域
    def output_new_add_risk_blocks(self):
        new_risk_blocks = {}
        str_time = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        f_name = u"{0}RiskBlock_{1}.txt".format(SpiderBase.TEMP_PATH, str_time)
        new_f_name = u"{0}NewRiskBlock_{1}.txt".format(SpiderBase.TEMP_PATH, str_time)

        last_str_time = time.strftime("%Y-%m-%d", time.localtime(time.time() - 3600 * 24))
        last_f_name = u"{0}RiskBlock_{1}.txt".format(SpiderBase.TEMP_PATH, last_str_time)

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

