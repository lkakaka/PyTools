
# -*- coding: utf-8 -*-

from spider_base import SpiderBase
from selenium.common.exceptions import NoSuchElementException
import re


class QuerySpider(SpiderBase):

    def __init__(self, show_browser=False):
        SpiderBase.__init__(self, show_browser)
        # 需要查询的省份
        self.query_filters = {}
        # get方式打开网页
        self.driver.get("http://bmfw.www.gov.cn/yqfxdjcx/index.html")
        # self.output_html()

        # close_elem = self.driver.find_element_by_class_name("closed")
        # if close_elem is not None:
        #     close_elem.click()

        self.container = self.driver.find_element_by_class_name("container")
        self.choose_box = self.driver.find_element_by_class_name("choose-box")
        self.simulate_query()

    def simulate_query(self):
        self.read_filter_blocks()
        province = self.choose_box.find_element_by_class_name("province")
        # print(province)
        provinces = province.find_elements_by_tag_name("li")

        try:
            for prov in provinces:
                if len(self.query_filters) > 0 and prov.text not in self.query_filters:
                    continue
                self.handle_province(prov)

            self.output_risk_record()
        except Exception as e:
            raise e
        finally:
            self.driver.quit()

    def handle_province(self, prov):
        # prov = self.provinces[self.cur_prov_idx]
        prov.click()
        self.sleep()
        query_citys = self.query_filters.get(prov.text)
        city_elem = self.choose_box.find_element_by_class_name("city")
        city_lst = city_elem.find_elements_by_tag_name("li")
        for city in city_lst:
            if query_citys is not None and len(query_citys) > 0 and city.text not in query_citys:
                continue
            self.handle_city(prov, city)

    def handle_city(self, prov, city):
        city.click()
        self.sleep()
        query_citys = self.query_filters.get(prov.text)
        query_blocks = None
        if query_citys is not None:
            query_blocks = query_citys.get(city.text)
        block_elem = self.choose_box.find_element_by_class_name("block")
        block_lst = block_elem.find_elements_by_tag_name("li")
        for block in block_lst:
            if query_blocks is not None and len(query_blocks) > 0 and block.text not in query_blocks:
                continue
            self.handle_block(prov, city, block)

    def handle_block(self, prov, city, block):
        block.click()
        self.sleep()
        # search_content = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "search-content")))

        choose_prov = self.choose_box.find_element_by_css_selector('.choose-tit.provinc')
        choose_city = self.choose_box.find_element_by_css_selector('.choose-tit.cityName')
        block_elem = self.choose_box.find_element_by_class_name("block")
        choose_block = block_elem.find_element_by_class_name("active")
        full_block_name = choose_prov.text + " " + choose_city.text + choose_block.text

        risk_table = None
        # 如果risk-table元素不存在,后面的find_element_by_class_name非常耗时
        if self.driver.page_source.find("risk-table") > 0:
            # st = time.time()
            try:
                risk_table = self.container.find_element_by_class_name('risk-table')
            except NoSuchElementException as e:
                risk_table = None

            # print("time={0}".format(time.time() - st))
        time_date = self.container.find_element_by_class_name('timeDate')
        self.set_result_time(time_date.text)

        if risk_table is not None:
            self.output_html()
            tbody = risk_table.find_element_by_tag_name("tbody")
            lines = tbody.find_elements_by_tag_name("tr")
            for line in lines:
                cols = line.find_elements_by_tag_name("td")
                full_block_name1 = full_block_name + cols[0].text
                print(full_block_name1 + " " + cols[1].text + " " + time_date.text)
                self.add_risk_block(cols[1].text, full_block_name, cols[0].text)
        else:
            search_content = self.choose_box.find_element_by_class_name("search-content")
            result = search_content.find_element_by_tag_name('span')
            print(full_block_name + ":" + result.text + " " + time_date.text)

            self.add_risk_block(result.text, full_block_name, u"全域")

    def read_filter_blocks(self):
        f_name = u"{0}query_blocks.ini".format(SpiderBase.TEMPLATE_PATH)
        f = open(f_name, 'r')
        for line in f.readlines():
            if line.startswith("#"):
                continue
            # print(line)
            lst = line.split(" ")
            prov = None
            city = None
            for idx in range(len(lst)):
                if idx == 0:
                    prov = lst[idx]
                    if prov not in self.query_filters:
                        self.query_filters[prov] = {}
                if idx == 1:
                    citys = lst[idx].split(",")
                    for city in citys:
                        if city not in self.query_filters[prov]:
                            self.query_filters[prov][city] = []
                    if len(citys) > 1:
                        continue
                    city = citys[0]

                if idx == 2:
                    for block in lst[idx].split(","):
                        lst_block = self.query_filters[prov][city]
                        if block not in lst_block:
                            lst_block.append(block)
        print("查询地区:")
        print(self.query_filters)
        f.close()


if __name__ == '__main__':
    show_browser = True
    import sys
    if len(sys.argv) > 1:
        show_browser = True if sys.argv[1] == "1" else False
    QuerySpider(show_browser)
