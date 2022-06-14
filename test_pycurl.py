#!/usr/bin/python
# -*- coding:UTF-8 -*-
import json
import os, sys
import time
import StringIO

import pycurl

# 探测的目标URL
# URL = "http://www.baidu.com"
URL = "http://api3.ksapisrv.com/rest/n/user/profile/v2?c=BETA&did=AAB4E9D1-D3D0-4CCA-A1F9-2DA770A7A493&userRecoBit=0&kpn=KUAISHOU&deviceBit=0&grant_browse_type=AUTHORIZED&keyconfig_state=2&sw=1125&is_background=0&kpf=IPHONE&sys=ios14.4&sh=2436&kcv=1462&browseType=4&net=%E4%B8%AD%E5%9B%BD%E7%94%B5%E4%BF%A1_5&darkMode=false&ver=10.5&mod=iPhone11%2C2&ud=2305071308&isp=CTCC&cold_launch_time_ms=1654680527152&vague=0&egid=DFPE8CEFA0D1E518114153B0B0B2C7EDBE737B5064C66B5C4E3EE5437C54A4F8&appver=10.5.10.991037"
payload = {
        "__NS_sig3": "2c3d4e7e91bb6e78564b676653f661fcdc0fde1c79757b6d",
        "__NStokensig": "9faad4649afa2c61f28e35dc4b6365fb5c342fe8db97c2ac93acb441d70249e1",
        "client_key": "56c3713c",
        "country_code": "cn",
        "cs": "true",
        "global_id": "DFPEF91EB86C15C846D5DBAC89D109B7CA3C25A205CDEBE30F8CE5D072B37F56",
        "kuaishou.api_st": "Cg9rdWFpc2hvdS5hcGkuc3QSoAF4dkz6CziiDIiZeNeazO7Ln2-xAl2fgIRxY9coOqpKQ7Y4kOfB1bfF_OnbUmnUdfv3eG9rxWIvlrFUryMOGpqJCHjE8YWSjLxquWbUZFDoRmus6588rPspY6AxquxNq24j_0_MxcqKju04mkP-8LG6cAMtXe7oR5ERqaud-oO6eTMiscJEsJCjQEKe4jCs0APzF2XeVaZG-vrJSFmXY0_bGhJEJSDbmRFB8aBbsn7UJvfzpQciIAo5-USell2_gjhvlqkhE8jQycYSOPuaWGv9cem01QIdKAUwAQ",
        "language": "zh-Hans-CN;q=1",
        "power_mode": "0",
        "pv": "1",
        "scene": "5",
        "selfMixed": "0",
        "sig": "85c0a153221fd8072f2569551ff911ad",
        "thermal": "10000",
        "token": "c387a6eeff37423f83d2e7c45ebdff61-2305071308",
        "uQaTag": "0",
        "user": "2305071308",
        "version": "2"
    }
headers ={
"Accept": "application/json",
"Accept-Encoding": "gzip, deflate",
"Accept-Language": "zh-Hans-CN;q=1",
"Content-Length": "792",
"Content-Type": "application/x-www-form-urlencoded",
"Cookie": "__NSWJ=79zocO5Ev4g7v4qQvxTkbkHHbkBKQDZXtpeJF+od8nR4luTer66hXyA0auG+9LvGAAAABA==;region_ticket=RT_DD0F5E574A4900092CC0BD2FC6608914DB474A71436012F07BE36C01468B9E427B4E915D8",
"Host": "127.0.0.1",
"Lyrebird-Client-Address": "172.17.214.6",
"Mitmproxy-Proxy": "172.17.214.6",
"Proxy-Connection": "keep-alive",
"User-Agent": "kwai-ios",
"X-Client-Info": "model=iPhone11,2;os=iOS;nqe-score=17;network=WIFI;",
"X-KTrace-Id-Enabled": "0",
"X-REQUESTID": "165468056838377086",
"X-Ref-Page": "MY_PROFILE"
}
headers_list=[]
for key in  headers.keys():
    str=f'{key}:{headers.get(key)}'
    headers_list.append(str)


print("headers_list:",headers_list)

# 创建一个Curl对象
c = pycurl.Curl()

# 定义请求的URL常量
c.setopt(pycurl.URL, URL)
c.setopt(pycurl.HTTPHEADER, headers_list)


c.setopt(pycurl.POST, 1)
data = json.dumps(payload)
body_as_json_string = data
body_as_file_object = StringIO(body_as_json_string)

# prepare and send. See also: pycurl.READFUNCTION to pass function instead
c.setopt(pycurl.READDATA, body_as_file_object)
# c.setopt(pycurl.POSTFIELDS, data)
# 定义请求连接的等待时间
c.setopt(pycurl.CONNECTTIMEOUT, 5)
# 定义请求超时时间
c.setopt(pycurl.TIMEOUT, 5)
# 屏蔽下载进度条
c.setopt(pycurl.NOPROGRESS, 1)
# 完成交互后强制断开连接，不重用
c.setopt(pycurl.FORBID_REUSE, 1)

# 指定HTTP重定向的最大数为1
c.setopt(pycurl.MAXREDIRS, 1)
# 设置保存DNS信息的时间为30秒
c.setopt(pycurl.DNS_CACHE_TIMEOUT, 30)
# 创建一个文件对象，以“wb”方式打开，用来存储返回的http头部及页面内容
file_path=os.path.dirname(os.path.realpath(__file__)) + "/content.txt"
print("file_path:",file_path)
indexfile = open(file_path, "wb")
# 将返回的HTTP HEADER定向到indexfile文件
c.setopt(pycurl.WRITEHEADER, indexfile)
# 将返回的HTML内容定向到indexfile文件对象
c.setopt(pycurl.WRITEDATA, indexfile)
try:
    # 提交请求
    c.perform()
except Exception as e:
    indexfile.close()
    c.close()
    sys.exit()

# 获取DNS解析时间
NAMELOOKUP_TIME = c.getinfo(c.NAMELOOKUP_TIME)
# 获取建立连接时间
CONNECT_TIME = c.getinfo(c.CONNECT_TIME)
# 获取从建立连接到准备传输所消耗的时间
PRETRANSFER_TIME = c.getinfo(c.PRETRANSFER_TIME)
# 获取从建立连接到传输开始消耗的时间
STARTTRANSFER_TIME = c.getinfo(c.STARTTRANSFER_TIME)
# 获取传输的总时间
TOTAL_TIME = c.getinfo(c.TOTAL_TIME)
# 获取HTTP状态码
HTTP_CODE = c.getinfo(c.HTTP_CODE)
# 获取下载数据包大小
SIZE_DOWNLOAD = c.getinfo(c.SIZE_DOWNLOAD)
# 获取HTTP头部大小
HEADER_SIZE = c.getinfo(c.HEADER_SIZE)
# 获取平均下载速度
SPEED_DOWNLOAD = c.getinfo(c.SPEED_DOWNLOAD)
# 打印输出相关数据
print("HTTP状态码： %d" % (HTTP_CODE))
print("DNS解析时间: %.2f ms" % (NAMELOOKUP_TIME * 1000))
print("建立连接时间： %.2f ms" % (CONNECT_TIME * 1000))
print("准备传输时间： %.2f ms" % (PRETRANSFER_TIME * 1000))
print("传输开始时间: %.2f ms" % (STARTTRANSFER_TIME * 1000))
print("传输结束总时间： %.2f ms" % (TOTAL_TIME * 1000))
print("下载数据包大小： %d bytes/s" % (SIZE_DOWNLOAD))
print("HTTP头部大小： %d byte" % (HEADER_SIZE))
print("平均下载速度： %d bytes/s" % (SPEED_DOWNLOAD))
# 关闭文件及Curl对象
indexfile.close()
c.close()
