
# -*- coding: utf-8 -*-

from spider_base import SpiderBase
from spider_base import RiskLevel
import re
import datetime


class ResultSpider(SpiderBase):
    def __init__(self, show_brower=False):
        SpiderBase.__init__(self, show_brower)
        try:
            self.query_risk_block()
        except Exception as e:
            raise e
        finally:
            self.driver.close()

    def query_risk_block(self):
        # self.read_record_from_file("RiskBlock_2021-01-21.txt")
        # if True:
        #     return
        # get方式打开网页
        print(u"正在获取网页信息...")
        self.driver.get("http://bmfw.www.gov.cn/yqfxdjcx/risk.html")
        # self.output_html()
        r_header = self.driver.find_element_by_class_name('r-header')
        r_time = r_header.find_element_by_class_name("r-time")
        print(r_time.text)
        self.set_result_time(r_time.text)
        divs = r_header.find_elements_by_tag_name("div")
        for div in divs:
            div.click()
            self.sleep()
            # span = div.find_element_by_tag_name("span")
            print(div.text)
            cls_attr = div.get_attribute("class")
            if cls_attr.find("r-high") >= 0:
                self.get_risk_block(True)
            else:
                self.get_risk_block(False)
            print("")
        self.output_risk_record()

    def get_risk_block(self, is_high):
        prefix = "h" if is_high else "m"
        while True:
            self.handle_one_risk_page(is_high)
            content = self.driver.find_element_by_class_name(prefix + "-content")
            pages_box = content.find_element_by_class_name("pages-box")
            cur_btn = pages_box.find_element_by_class_name("current")
            next_btn_text = str(int(cur_btn.text) + 1)
            page_btns = pages_box.find_elements_by_tag_name("button")
            next_btn = None
            for page_btn in page_btns:
                if page_btn.text == next_btn_text:
                    next_btn = page_btn
                    break

            if next_btn is None:
                break
            next_btn.click()
            self.sleep()

    def handle_one_risk_page(self, is_high):
        prefix = "h" if is_high else "m"
        risk_text = RiskLevel.HIGH_LV_TEXT if is_high else RiskLevel.MEDIUM_LV_TEXT
        container = self.driver.find_element_by_class_name(prefix + "-container")
        headers = container.find_elements_by_class_name(prefix + "-header")
        for header in headers:
            table = header.find_element_by_class_name(prefix + "-table")
            style = table.get_attribute("style")
            # print(style)
            texts = header.text.split("\n")
            city_name = texts[0]
            city_info = city_name.split(" ")
            city_name = city_info[0] + city_info[1]
            if style == "display: none;":
                # print(city_name)
                block_name = city_info[2] + u"全域"
                self.add_risk_block(risk_text, city_name, block_name)
            else:
                trs = table.find_elements_by_tag_name("tr")
                for tr in trs:
                    h_td1 = tr.find_element_by_class_name(prefix + "-td1")
                    block_name = city_info[2] + h_td1.text
                    # print(city_name)
                    # print(block_name)
                    self.add_risk_block(risk_text, city_name, block_name)


if __name__ == '__main__':
    show_browser = True
    import sys
    if len(sys.argv) > 1:
        show_browser = True if sys.argv[1] == "1" else False
    ResultSpider(show_browser)
