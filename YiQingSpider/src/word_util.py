# -*- coding: utf-8 -*-

from docx import Document

from spider_base import RiskBlock
from spider_base import SpiderBase
import re


class WordUtil(object):
    @staticmethod
    def read_word():
        text = u"截至2021-02-01 15时，全国疫情："
        matchObj = re.match(r'\D+(\d+-\d+-\d+ \d+).*', text)
        if matchObj:
            print(matchObj)
            print(matchObj.group(1))

        # doc = Document(u'../关于发布国内疫情风险等级提示的通知（截至2月2日15时）.docx')
        SpiderBase.read_record_from_word(u'../关于发布国内疫情风险等级提示的通知（截至2月1日15时）.docx')
        # paragraphs = doc.paragraphs
        # # pars_string = [par.text for par in paragraphs]
        # # print(pars_string)
        # idx = 0
        # for par in paragraphs:
        #     print("{0}:{1}".format(idx, par.text))
        #     idx += 1
        #     # for run in par.runs:
        #     #     # run.text = run.text+"new"
        #     #     print(run.text)
        #     #     # run.text = run.text.replace("NewMediumRiskBlock", "dsfsdafasdf")
        # doc.save(u"../test_bak.docx")

        # lst = []
        # risk_block = RiskBlock(u"北京", "你好")
        # lst.append(risk_block)
        # risk_block1 = RiskBlock(u"北京", "你好")
        # if risk_block1 in lst:
        #     print("已经存在")

    @staticmethod
    def write_word():
        pass


if __name__ == '__main__':
    WordUtil.read_word()
