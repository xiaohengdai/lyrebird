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

from lyrebird import event
import os
import copy
from lyrebird import on_response, log
from lyrebird.case_strategy.mock_case_stratergy import *
from util.file_util import  get_file_type_replace_robust_checkers_config_path_value

logger = log.get_logger()




# THRESHOLD_IMG_SIZE: image size limitation


def ignore_check(msg):
    if 'name' in msg.keys():
        if msg['name'] != 'server.response':
            return True
        if 'response' not in msg['flow']:
            return True
        if 'image' not in msg['flow']['response']['headers']['Content-Type']:
            return True
    return False

@on_response()
def random_value_robust(flow):
    flow_request = flow['request']
    flow_response = flow['response']
    logger.info("flow_request:" + str(flow_request))
    # logger.info("flow_request.get('url'):" + str(flow_request.get('url')))
    flow_path=flow_request.get('path')
    logger.info("flow_path:" + str(flow_path))
    # logger.info("origin_flow_response0:" + str(flow_response))
    # logger.info("flow_client_address:" + str(flow_client_address))
    # mock_flow_response = copy.deepcopy(flow_response)
    url_list = get_file_type_replace_robust_checkers_config_path_value("url_list")
    mock_flow_response = flow_response
    if len(url_list)==0:
        logger.info("对所有url进行随机Mock")
    else:
        if flow_path in url_list:
            logger.info("当前url在需要Mock的url配置文件中")
            logger.info("flow_path:"+str(flow_path))
            url_key_value=get_file_type_replace_robust_checkers_config_path_value("url_key_value")
            flow_url_key_value=url_key_value.get(flow_path)
            if not flow_url_key_value:
                logger.info("file_type_replace_robust_checkers_config.yaml文件中没有配置当前flow_url的key_value信息，针对当前url无特殊处理逻辑")
            mock_key_value=flow_url_key_value
            #需要在这里加随机Mock策略，先判断数据类型、文件格式，然后再针对性的mock

            mock_flow_response = set_per_key_value(flow_response,mock_key_value,mock_type=2)
            if flow_response != mock_flow_response:
                logger.info("数据Mock成功")
                # logger.info("data_json:"+str(data_json))
                # logger.info("copy_data_json:"+str(copy_data_json))
            else:
                logger.info("没有对数据进行Mock")
            logger.info("mock_flow_response:" + str(mock_flow_response))

        else:
            logger.info("当前url不在需要Mock的url配置文件中")
    flow['response'] = mock_flow_response





