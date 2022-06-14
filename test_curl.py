
import curlify

import requests
import json
#目前看api3的域名使用这种方式没有问题
url = "http://api3.ksapisrv.com/rest/n/user/profile/v2?c=BETA&did=AAB4E9D1-D3D0-4CCA-A1F9-2DA770A7A493&userRecoBit=0&kpn=KUAISHOU&deviceBit=0&grant_browse_type=AUTHORIZED&keyconfig_state=2&sw=1125&is_background=0&kpf=IPHONE&sys=ios14.4&sh=2436&kcv=1462&browseType=4&net=%E4%B8%AD%E5%9B%BD%E7%94%B5%E4%BF%A1_5&darkMode=false&ver=10.5&mod=iPhone11%2C2&ud=2305071308&isp=CTCC&cold_launch_time_ms=1654680527152&vague=0&egid=DFPE8CEFA0D1E518114153B0B0B2C7EDBE737B5064C66B5C4E3EE5437C54A4F8&appver=10.5.10.991037"

# url = "http://apijs1.ksapisrv.com/rest/n/user/profile/v2?c=BETA&did=AAB4E9D1-D3D0-4CCA-A1F9-2DA770A7A493&kpn=KUAISHOU&grant_browse_type=AUTHORIZED&deviceBit=0&keyconfig_state=2&userRecoBit=0&sw=1125&is_background=0&kpf=IPHONE&sys=ios14.4&sh=2436&kcv=1462&browseType=4&net=%E4%B8%AD%E5%9B%BD%E7%94%B5%E4%BF%A1_5&darkMode=false&ver=10.5&mod=iPhone11%2C2&ud=2305071308&isp=CTCC&cold_launch_time_ms=1654680527152&vague=0&egid=DFPE8CEFA0D1E518114153B0B0B2C7EDBE737B5064C66B5C4E3EE5437C54A4F8&appver=10.5.10.991037"
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

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)



print(response.request)
print(curlify.to_curl(response.request,compressed=True))