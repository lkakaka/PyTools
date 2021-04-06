# -*- coding: UTF-8 -*-
# Python 2.x引入httplib模块。
# import httplib
# Python 3.x引入http.client模块。
import http.client
# Python 2.x引入urllib模块。
# import urllib
# Python 3.x引入urllib.parse模块。
import urllib.parse
import json
# pip install playsound
from playsound import playsound
# pip install aliyun-python-sdk-core==2.13.3 # 安装阿里云SDK核心库（获取token）
import os
import time


class AlyTTS(object):
    APP_KEY = 'DGkmkLH5RTst84Vp'
    TOKEN = 'b5985bafc5ee4e97861cc3f29dc1fb9b'

    @staticmethod
    def get_token():
        from aliyunsdkcore.client import AcsClient
        from aliyunsdkcore.request import CommonRequest

        # 创建AcsClient实例
        client = AcsClient(
            "<您的AccessKey Id>",
            "<您的AccessKey Secret>",
            "cn-shanghai"
        )

        # 创建request，并设置参数。
        request = CommonRequest()
        request.set_method('POST')
        request.set_domain('nls-meta.cn-shanghai.aliyuncs.com')
        request.set_version('2019-02-28')
        request.set_action_name('CreateToken')
        response = client.do_action_with_exception(request)

        # 调用云端服务的返回
        # {
        #     "NlsRequestId": "aed8c1af075347819118ff6bf811****",
        #     "RequestId": "0989F63E-5069-4AB0-822B-5BD2D953****",
        #     "Token": {
        #         "ExpireTime": 1527592757,
        #         "Id": "124fc7526f434b8c8198d6196b0a****",
        #         "UserId": "12345678****"
        #     }
        # }

        print(response)

    @staticmethod
    def process_get_request(app_key, token, text, audio_save_file, file_format, sample_rate):
        host = 'nls-gateway.cn-shanghai.aliyuncs.com'
        url = 'https://' + host + '/stream/v1/tts'
        # 设置URL请求参数
        url = url + '?appkey=' + app_key
        url = url + '&token=' + token
        url = url + '&text=' + text
        url = url + '&format=' + file_format
        url = url + '&sample_rate=' + str(sample_rate)
        # voice 发音人，可选，默认是xiaoyun。
        # url = url + '&voice=' + 'xiaoyun'
        # volume 音量，范围是0~100，可选，默认50。
        # url = url + '&volume=' + str(50)
        # speech_rate 语速，范围是-500~500，可选，默认是0。
        # url = url + '&speech_rate=' + str(0)
        # pitch_rate 语调，范围是-500~500，可选，默认是0。
        # url = url + '&pitch_rate=' + str(0)
        print(url)
        # Python 2.x请使用httplib。
        # conn = httplib.HTTPSConnection(host)
        # Python 3.x请使用http.client。
        conn = http.client.HTTPSConnection(host)
        conn.request(method='GET', url=url)
        # 处理服务端返回的响应。
        response = conn.getresponse()
        print('Response status and response reason:')
        print(response.status, response.reason)
        content_type = response.getheader('Content-Type')
        print(content_type)
        body = response.read()
        if 'audio/mpeg' == content_type:
            with open(audio_save_file, mode='wb') as f:
                f.write(body)
            print('The GET request succeed!')
        else:
            print('The GET request failed: ' + str(body))
        conn.close()

    @staticmethod
    def process_post_request(app_key, token, text, audio_save_file, file_format, sample_rate):
        host = 'nls-gateway.cn-shanghai.aliyuncs.com'
        url = 'https://' + host + '/stream/v1/tts'
        # 设置HTTPS Headers。
        http_headers = {
            'Content-Type': 'application/json'
        }
        # 设置HTTPS Body。
        body = {'appkey': app_key, 'token': token, 'text': text, 'format': file_format, 'sample_rate': sample_rate}
        body = json.dumps(body)
        print('The POST request body content: ' + body)
        # Python 2.x请使用httplib。
        # conn = httplib.HTTPSConnection(host)
        # Python 3.x请使用http.client。
        conn = http.client.HTTPSConnection(host)
        conn.request(method='POST', url=url, body=body, headers=http_headers)
        # 处理服务端返回的响应。
        response = conn.getresponse()
        print('Response status and response reason:')
        print(response.status, response.reason)
        content_type = response.getheader('Content-Type')
        print(content_type)
        body = response.read()
        if 'audio/mpeg' == content_type:
            with open(audio_save_file, mode='wb') as f:
                f.write(body)
            print('The POST request succeed!')
        else:
            print('The POST request failed: ' + str(body))
        conn.close()

    @staticmethod
    def read_text(text):
        print("start read text " + text)
        # 采用RFC 3986规范进行urlencode编码。
        text_url_encode = text
        # Python 2.x请使用urllib.quote。
        # text_url_encode = urllib.quote(text_url_encode, '')
        # Python 3.x请使用urllib.parse.quote_plus。
        text_url_encode = urllib.parse.quote_plus(text_url_encode)
        text_url_encode = text_url_encode.replace("+", "%20")
        text_url_encode = text_url_encode.replace("*", "%2A")
        text_url_encode = text_url_encode.replace("%7E", "~")
        print('text: ' + text_url_encode)
        audio_save_file = 'syAudio.wav'
        file_format = 'wav'
        sample_rate = 16000
        # GET请求方式
        AlyTTS.process_get_request(AlyTTS.APP_KEY, AlyTTS.TOKEN, text_url_encode, audio_save_file, file_format, sample_rate)
        # POST请求方式
        # process_post_request(AlyTTS.APP_KEY, AlyTTS.TOKEN, text, audio_save_file, file_format, sample_rate)
        playsound(audio_save_file, block=True)
        print("end read text " + text)


if __name__ == "__main__":
    txt = '这是什么鬼东西'
    AlyTTS.read_text(txt)
