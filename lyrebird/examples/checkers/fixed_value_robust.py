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
from util.file_util import get_checkers_config_value

logger = log.get_logger()




# THRESHOLD_IMG_SIZE: image size limitation



@on_response()
def fixed_value_robust(flow):
    # print('mock_flow_response1:',mock_flow_response)
    # print("type(flow['ResponseBody']):", type(flow['ResponseBody']))
    # logger.info("flow:" + str(flow))
    # logger.info("flow.keys():"+str(flow.keys()))
    # flow_id = flow['id']
    # flow_size = flow['size']
    # flow_duration = flow['duration']
    # flow_start_time = flow['start_time']
    flow_request = flow['request']
    flow_response = flow['response']
    # flow_client_address = flow['client_address']
    # logger.info("flow_id:" + str(flow_id))
    # logger.info("flow_size:" + str(flow_size))
    # logger.info("flow_duration:" + str(flow_duration))
    # logger.info("flow_start_time:" + str(flow_start_time))
    logger.info("flow_request:" + str(flow_request))
    # logger.info("flow_request.get('url'):" + str(flow_request.get('url')))
    flow_path=flow_request.get('path')
    logger.info("flow_path:" + str(flow_path))
    url_list = get_checkers_config_value("url_list")
    mock_flow_response = flow_response
    if len(url_list)==0:
        logger.info("对所有url进行Mock")
    else:
        if flow_path in url_list:
            logger.info("当前url在需要Mock的url配置文件中")
            logger.info("flow_path:"+str(flow_path))
            url_key_value=get_checkers_config_value("url_key_value")
            flow_url_key_value=url_key_value.get(flow_path)
            if not flow_url_key_value:
                logger.info("checkers_config.yaml文件中没有配置当前flow_url的key_value信息，针对当前url无特殊处理逻辑")
            mock_key_value=flow_url_key_value
            mock_flow_response = set_per_key_value(flow_response,mock_key_value,mock_type=0)
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





