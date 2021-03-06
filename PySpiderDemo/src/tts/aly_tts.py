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
# pip install aliyun-python-sdk-core==2.13.3 # 安装阿里云SDK核心库（获取token）
from src.tts.tts_base import TTSBase
import time


class AlyTTS(TTSBase):
    APP_KEY = 'DGkmkLH5RTst84Vp'
    AUDIO_FILE = "audio.wav"

    def __init__(self):
        self._token = ""
        self._token_expire_time = 0
        self.get_token()

    def get_token(self):
        if self._token_expire_time - time.time() > 60:
            return
        from aliyunsdkcore.client import AcsClient
        from aliyunsdkcore.request import CommonRequest

        # 创建AcsClient实例
        client = AcsClient(
            "LTAI5tLKcEUa1AH5eLhKoYuL",  # <您的AccessKey Id>,
            "W81JYe6HswKjB30hluROnRCOcrj5Qv",  # 您的AccessKey Secret
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
        res_dict = json.loads(response)
        token_info = res_dict.get("Token", {})
        self._token = token_info.get("Id", "")
        self._token_expire_time = token_info.get("ExpireTime", 0)

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
        is_success = False
        if 'audio/mpeg' == content_type:
            with open(audio_save_file, mode='wb') as f:
                f.write(body)
                is_success = True
            print('The GET request succeed!')
        else:
            print('The GET request failed: ' + str(body))
        conn.close()
        return is_success

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

    def translate_text(self, text):
        self.get_token()
        # print("start read text " + text)
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
        audio_save_file = TTSBase.WAV_SAVE_FILE
        file_format = 'wav'
        sample_rate = 16000
        # GET请求方式
        is_success = AlyTTS.process_get_request(AlyTTS.APP_KEY, self._token, text_url_encode, audio_save_file,
                                                file_format, sample_rate)
        # POST请求方式
        # process_post_request(AlyTTS.APP_KEY, self._token, text, audio_save_file, file_format, sample_rate)
        # print("end read text " + text)
        return is_success, audio_save_file


if __name__ == "__main__":
    txt = '这是什么鬼东西'
    AlyTTS().translate_text(txt)
    from playsound import playsound
    playsound(TTSBase.WAV_SAVE_FILE, block=True)
