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


# HIGH_RISK_LEVEL = u"高风险区"
# MEDIUM_RISK_LEVEL = u"中风险区"
#
#
# class YiQingSpider(object):
#     def __init__(self, show_browser):
#         # 需要查询的省份
#         self.query_filters = {}
#         self.QUERY_PROVINCES = {"河北": {"石家庄市": []}}
#         self.QUERY_CITIES = []#[u"石家庄市"]
#         self.QUERY_BLOCKS = []#[u"藁城区"]
#
#         self.risk_blocks = {}
#
#         self._flag = False
#         self._wait_time = 1.5
#
#         self.container = None
#         self.choose_box = None
#         self._init_driver(show_browser)
#         # 模拟查询
#         # self.simulate_query()
#
#         # 直接查询风险地区页面
#         self.query_risk_block()
#
#     def _init_driver(self, show_browser):
#         if show_browser:
#             # 创建可见的Chrome浏览器， 方便调试
#             self.driver = webdriver.Chrome()
#         else:
#             # 创建Chrome的无头浏览器
#             opt = webdriver.ChromeOptions()
#             opt.headless = True
#             self.driver = webdriver.Chrome(options=opt)
#
#         self.driver.implicitly_wait(10)
#
#     def sleep(self):
#         if self._wait_time <= 0:
#             return
#         time.sleep(self._wait_time)
#
#     def output_html(self):
#         soup = BeautifulSoup(self.driver.page_source, 'html.parser')
#         print(soup.prettify())
#
#     def query_risk_block(self):
#         # get方式打开网页
#         self.driver.get("http://bmfw.www.gov.cn/yqfxdjcx/risk.html")
#         self.output_html()
#
#         r_header = self.driver.find_element_by_class_name('r-header')
#         r_time = r_header.find_element_by_class_name("r-time")
#         print(r_time.text)
#         divs = r_header.find_elements_by_tag_name("div")
#         for div in divs:
#             div.click()
#             self.sleep()
#             # span = div.find_element_by_tag_name("span")
#             print(div.text)
#             cls_attr = div.get_attribute("class")
#             if cls_attr.find("r-high") >= 0:
#                 self.get_risk_block(True)
#             else:
#                 self.get_risk_block(False)
#             print("\n")
#         print("-----------------output----------------")
#         self.output_risk_record()
#         self.driver.quit()
#
#     def get_risk_block(self, is_high):
#         prefix = "h" if is_high else "m"
#         while True:
#             self.handle_one_risk_page(is_high)
#             content = self.driver.find_element_by_class_name(prefix + "-content")
#             pages_box = content.find_element_by_class_name("pages-box")
#             cur_btn = pages_box.find_element_by_class_name("current")
#             next_btn_text = str(int(cur_btn.text) + 1)
#             page_btns = pages_box.find_elements_by_tag_name("button")
#             next_btn = None
#             for page_btn in page_btns:
#                 if page_btn.text == next_btn_text:
#                     next_btn = page_btn
#                     break
#
#             if next_btn is None:
#                 break
#             next_btn.click()
#             self.sleep()
#
#     def handle_one_risk_page(self, is_high):
#         prefix = "h" if is_high else "m"
#         risk_level = HIGH_RISK_LEVEL if is_high else MEDIUM_RISK_LEVEL
#         container = self.driver.find_element_by_class_name(prefix + "-container")
#         headers = container.find_elements_by_class_name(prefix + "-header")
#         for header in headers:
#             table = header.find_element_by_class_name(prefix + "-table")
#             style = table.get_attribute("style")
#             # print(style)
#             texts = header.text.split("\n")
#             block_name = texts[0]
#             if style == "display: none;":
#                 print(block_name)
#                 self.add_risk_block(risk_level, block_name)
#             else:
#                 trs = table.find_elements_by_tag_name("tr")
#                 for tr in trs:
#                     h_td1 = tr.find_element_by_class_name(prefix + "-td1")
#                     print(block_name + h_td1.text)
#                     self.add_risk_block(risk_level, block_name + h_td1.text)
#
#     def read_filter_blocks(self):
#         f_name = u"./query_blocks.ini"
#         f = open(f_name, 'r')
#         for line in f.readlines():
#             if line.startswith("#"):
#                 continue
#             # print(line)
#             lst = line.split(" ")
#             prov = None
#             city = None
#             for idx in range(len(lst)):
#                 if idx == 0:
#                     prov = lst[idx]
#                     if prov not in self.query_filters:
#                         self.query_filters[prov] = {}
#                 if idx == 1:
#                     citys = lst[idx].split(",")
#                     for city in citys:
#                         if city not in self.query_filters[prov]:
#                             self.query_filters[prov][city] = []
#                     if len(citys) > 1:
#                         continue
#                     city = citys[0]
#
#                 if idx == 2:
#                     for block in lst[idx].split(","):
#                         lst_block = self.query_filters[prov][city]
#                         if block not in lst_block:
#                             lst_block.append(block)
#         print("查询地区:")
#         print(self.query_filters)
#         f.close()
#
#     def add_risk_block(self, risk_level, block_name):
#         if risk_level == u'低风险地区':
#             return
#         block_name = block_name.replace(" ", "")
#         lst_block = self.risk_blocks.get(risk_level)
#         if lst_block is None:
#             lst_block = []
#             self.risk_blocks[risk_level] = lst_block
#         if block_name in lst_block:
#             print(u"小区{0}已存在{1}中".format(block_name, risk_level))
#             return
#         lst_block.append(block_name)
#
#     def simulate_query(self):
#         self.read_filter_blocks()
#         """
#         开始爬虫
#         :return:
#         """
#         # get方式打开网页
#         self.driver.get("http://bmfw.www.gov.cn/yqfxdjcx/index.html")
#         # self.output_html()
#
#         # close_elem = self.driver.find_element_by_class_name("closed")
#         # if close_elem is not None:
#         #     close_elem.click()
#
#         self.container = self.driver.find_element_by_class_name("container")
#         self.choose_box = self.driver.find_element_by_class_name("choose-box")
#
#         province = self.choose_box.find_element_by_class_name("province")
#         # print(province)
#         provinces = province.find_elements_by_tag_name("li")
#
#         try:
#             for prov in provinces:
#                 # if len(self.QUERY_PROVINCES) > 0 and prov.text not in self.QUERY_PROVINCES:
#                 #     continue
#                 if len(self.query_filters) > 0 and prov.text not in self.query_filters:
#                     continue
#                 self.handle_province(prov)
#
#             self.output_risk_record()
#         except Exception as e:
#             raise e
#         finally:
#             self.driver.quit()
#
#     def output_risk_record(self):
#         print("\n\n")
#         str_time = time.strftime("%Y-%m-%d", time.localtime(time.time()))
#         f_name = u"./RiskBlock_{0}.txt".format(str_time)
#         f = open(f_name, 'w', encoding="utf8")
#         for risk, blocks in self.risk_blocks.items():
#             risk_block_count_str = risk + ":({0}个)".format(len(blocks))
#             f.writelines(risk_block_count_str + "\n")
#             print(risk_block_count_str)
#             for block_name in blocks:
#                 f.writelines(block_name + "\n")
#                 print(block_name)
#             f.writelines("\n")
#             print("\n")
#         f.close()
#
#     def handle_province(self, prov):
#         # prov = self.provinces[self.cur_prov_idx]
#         prov.click()
#         self.sleep()
#         query_citys = self.query_filters.get(prov.text)
#         city_elem = self.choose_box.find_element_by_class_name("city")
#         city_lst = city_elem.find_elements_by_tag_name("li")
#         for city in city_lst:
#             # if len(self.QUERY_CITIES) > 0 and city.text not in self.QUERY_CITIES:
#             #     continue
#             if query_citys is not None and len(query_citys) > 0 and city.text not in query_citys:
#                 continue
#             self.handle_city(prov, city)
#
#     def handle_city(self, prov, city):
#         city.click()
#         self.sleep()
#         query_citys = self.query_filters.get(prov.text)
#         query_blocks = None
#         if query_citys is not None:
#             query_blocks = query_citys.get(city.text)
#         block_elem = self.choose_box.find_element_by_class_name("block")
#         block_lst = block_elem.find_elements_by_tag_name("li")
#         for block in block_lst:
#             # if len(self.QUERY_BLOCKS) > 0 and block.text not in self.QUERY_BLOCKS:
#             #     continue
#             if query_blocks is not None and len(query_blocks) > 0 and block.text not in query_blocks:
#                 continue
#             self.handle_block(prov, city, block)
#
#     def handle_block(self, prov, city, block):
#         block.click()
#         self.sleep()
#         if not self._flag:
#             self.output_html()
#             self._flag = True
#         # search_content = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "search-content")))
#
#         choose_prov = self.choose_box.find_element_by_css_selector('.choose-tit.provinc')
#         choose_city = self.choose_box.find_element_by_css_selector('.choose-tit.cityName')
#         block_elem = self.choose_box.find_element_by_class_name("block")
#         choose_block = block_elem.find_element_by_class_name("active")
#         full_block_name = choose_prov.text + choose_city.text + choose_block.text
#
#         risk_table = None
#         # 如果risk-table元素不存在,后面的find_element_by_class_name非常耗时
#         if self.driver.page_source.find("risk-table") > 0:
#             # st = time.time()
#             try:
#                 risk_table = self.container.find_element_by_class_name('risk-table')
#             except NoSuchElementException as e:
#                 risk_table = None
#
#             # print("time={0}".format(time.time() - st))
#
#         if risk_table is not None:
#             tbody = risk_table.find_element_by_tag_name("tbody")
#             lines = tbody.find_elements_by_tag_name("tr")
#             for line in lines:
#                 cols = line.find_elements_by_tag_name("td")
#                 full_block_name1 = full_block_name + cols[0].text
#                 print(full_block_name1 + " " + cols[1].text)
#                 self.add_risk_block(cols[1].text, full_block_name1)
#         else:
#             search_content = self.choose_box.find_element_by_class_name("search-content")
#             result = search_content.find_element_by_tag_name('span')
#             time_date = search_content.find_element_by_class_name('timeDate')
#             print(full_block_name + ":" + result.text + " " + time_date.text)
#             self.add_risk_block(result.text, full_block_name)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    query()
    # show_browser = False
    # if len(sys.argv) > 1:
    #     show_browser = True if sys.argv[1] == "1" else False
    # YiQingSpider(show_browser)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
