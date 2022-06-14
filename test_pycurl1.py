"""
# !/usr/bin/env python
# @ItemName: PyCharm
# @File： HttpClient.py
# @Time：2022/6/9 22:46
# @Author：YuYe
"""
import json
import pycurl
import certifi
from io import BytesIO
# from tool.LogGer import logger
from urllib.parse import urlencode


class HttpClient(object):
    @staticmethod
    def client(
            method: str,
            url: str,
            headers: list,
            params: dict,
            **kwargs
    ) -> dict:
        """
        使用pycurl代替request发请求
        :param method: 请求方法
        :param url: 接口地址或者网页地址
        :param headers: 请求求信息
        :param params: 解决请求参数，如果是get请求或者其他传空字符串
        :param kwargs: 不定长参数
        :return: 返回一个字典类型，具体内容参考下方response字典数据结构
        """
        curl = pycurl.Curl()
        body_io = BytesIO()
        try:
            curl.setopt(pycurl.URL, url)
            curl.setopt(pycurl.WRITEDATA, body_io)
            curl.setopt(pycurl.SSL_VERIFYPEER, 0)
            curl.setopt(pycurl.SSL_VERIFYPEER, 0)
            curl.setopt(pycurl.SSL_VERIFYHOST, 0)
            curl.setopt(pycurl.FOLLOWLOCATION, 1)
            curl.setopt(pycurl.CAINFO, certifi.where())
            curl.setopt(pycurl.HTTPHEADER, headers)
            if method == "post":
                curl.setopt(pycurl.POST, 1)
                # 处理post不同类型数据请求
                if 'Content-Type: application/json' in headers:
                    if isinstance(params, dict):
                        curl.setopt(pycurl.POSTFIELDS, json.dumps(params))
            elif method == 'delete':
                curl.setopt(pycurl.CUSTOMREQUEST, method)
            elif method == 'head':
                curl.setopt(pycurl.HEADER, True)
                curl.setopt(pycurl.NOBODY, True)
            else:
                url = '{0}?{1}'.format(url, urlencode(params, True))
        except:
            # logger.info("代码出现bug")
            print("代码出现bug")
        finally:
            curl.perform()
            # logger.info("当前接口请求信息%s_%s_%s_%s" % (method, url, headers[0], params))
            print("当前接口请求信息%s_%s_%s_%s" % (method, url, headers[0], params))
            response = {
                'http_code': curl.getinfo(pycurl.HTTP_CODE),
                'body': body_io.getvalue().decode("utf-8"),
                'request': {
                    'method': method,
                    'url': url,
                    'params': params
                },
                'analyze': {
                    'NAMELOOKUP_TIME': curl.getinfo(curl.NAMELOOKUP_TIME),
                    'CONNECT_TIME': curl.getinfo(curl.CONNECT_TIME),
                    'PRETRANSFER_TIME': curl.getinfo(curl.PRETRANSFER_TIME),
                    'STARTTRANSFER_TIME': curl.getinfo(curl.STARTTRANSFER_TIME),
                    'TOTAL_TIME': curl.getinfo(curl.TOTAL_TIME),
                    'SIZE_DOWNLOAD': curl.getinfo(curl.SIZE_DOWNLOAD),
                    'HEADER_SIZE': curl.getinfo(curl.HEADER_SIZE),
                    'SPEED_DOWNLOAD': curl.getinfo(curl.SPEED_DOWNLOAD)

                },
                **kwargs
            }
            # 主要解决pytest运行打印log首行
            print("")
            return response
