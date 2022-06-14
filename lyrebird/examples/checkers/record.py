"""
checker example

steps:
- ignore unexepcted object
- prepare useful info
- check data

Info used in channel flow
├── name
└─┬ flow
  ├── size
  ├─┬ request
  │ └── url
  └─┬ response
    └─┬ headers
      └── Content-Type

"""
import curlify

from lyrebird import event
import os
import copy
from lyrebird import on_response, log
import csv
from lyrebird.case_strategy.mock_case_stratergy import *
from mitmproxy import ctx
from util.file_util import get_auto_mock_null_robust_config_value, update_auto_mock_null_robust_config_value
import time
logger = log.get_logger()




currentPath = os.path.abspath(os.path.dirname(__file__))
currentTime = time.strftime("%Y%m%d%H%M%S", time.localtime())
savePath = os.path.join(currentPath, currentTime + "-case.csv")
print("savePath:",savePath)
logger.info("savePath:"+str(savePath))



@on_response()
def record(flow):
    flow_request = flow['request']
    logger.info("flow_request:"+str(flow_request))
    flow_response = flow['response']
    logger.info("flow_response:"+str(flow_response))
    flow_path=flow_request.get('path')
    logger.info("flow_path:"+str(flow_path))
    method=flow_request.get('method')
    logger.info("method0:"+str(method))
    # 加上过滤条件
    if 'rest/' in str(flow_path): #只录制快手主站/极速版app内的
        # 打开保存在本地的数据文件
        requestInfo = {}
        requestInfo['request_url'] = str(flow_request.get("url"))

        data = flow_response.get("data")
        requestInfo['request_headers'] = create_headers(flow_request.get("headers"))
        requestInfo['request_query'] = create_headers(flow_request.get("query"))
        requestInfo['request_method'] = flow_request.get('method')
        requestInfo['status_code'] = flow_response.get('code')
        requestInfo['reason'] = flow_response.get('reason')
        requestInfo['response_data'] = data
        requestInfo['response_headers'] = create_headers(flow_response.get('headers'))
        requestInfo['request_time'] = flow_request.get("timestamp")

        requestInfo['response_time'] = flow_response.get('timestamp')
        requestInfo['scene_name'] = '主态点击粉丝列表进入'

        # requestInfo['response_time'] = requestInfo['response_time_end'] - requestInfo['request_time_start']  # 响应时间
        print(requestInfo)
        with open(savePath, 'a+') as csvfile:
            writer = csv.writer(csvfile)
            header_list = ["request_url", "request_headers", "request_query", "request_method", "status_code", "response_data", "response_time","scene_name"]
            writer.writerow(header_list)
            writer.writerows(
                [[requestInfo['request_url'], requestInfo['request_headers'],requestInfo['request_query'], requestInfo['request_method'],
                  requestInfo['status_code'], requestInfo['response_data'], requestInfo['response_time'],requestInfo['scene_name']]])
            # ctx.log('********************** 写入数据成功 ********************** ')
            logger.info("********************** 写入数据成功 ********************** ")

def create_headers(headers):
    """
    组装请求头
    :param headers:
    :return:
    """
    headersInfo = {}
    for k, v in headers.items():
        headersInfo[k] = v
    return headersInfo

def save_data(data, path):
    """
    保存数据
    :param data:
    :param path:
    :return:
    """
    header = list(data[0].keys())  # 数据列名
    with open(path, 'a+', newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writerows(data)  # 写入数据


