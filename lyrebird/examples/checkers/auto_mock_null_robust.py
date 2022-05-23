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
from util.file_util import get_auto_mock_null_robust_config_value, update_auto_mock_null_robust_config_value

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
    url_list = get_auto_mock_null_robust_config_value("url_list")
    mock_flow_response = flow_response
    if len(url_list)==0:
        logger.info("对所有url进行Mock")
    else:
        if flow_path in url_list:
            logger.info("当前url在需要Mock的url配置文件中")
            logger.info("flow_path:"+str(flow_path))
            url_key_value=get_auto_mock_null_robust_config_value("url_key_value")
            mock_file_path_li = []
            if url_key_value is not None:
                flow_url_key_value=url_key_value.get(flow_path)
                # mock_flow_response_dict = flow_url_key_value
                if not flow_url_key_value:
                    logger.info("checkers_config.yaml文件中没有配置当前flow_url的key_value信息，针对当前url无特殊处理逻辑")
                    flow_url_key_value[flow_path]["mock_file_path_li"] = []
                    flow_url_key_value[flow_path]["index"] = 0
                    flow_url_key_value[flow_path]["total_num"] = 0
                    index=0

                else:
                    mock_file_path_li = flow_url_key_value.get("mock_file_path_li")
                    index=int(flow_url_key_value.get("index"))
                    total_num=int(flow_url_key_value.get("total_num"))
                    logger.info("index:"+str(index))
            else:
                flow_url_key_value={}
                flow_url_key_value[flow_path]["mock_file_path_li"]=[]
                flow_url_key_value[flow_path]["index"]=0
                flow_url_key_value[flow_path]["total_num"] = 0
                index=0
                total_num=0
                # mock_flow_response_dict=flow_url_key_value
                logger.info("checkers_config.yaml文件中没有配置当前flow_url的key_value信息，针对当前url无特殊处理逻辑")

            # mock_flow_response = set_per_key_value(flow_response,mock_key_value,mock_type=0)

            index=int(index)
            mock_type = flow_url_key_value.get("mock_type")
            if mock_type is None:
                mock_type = 0
            else:
                mock_type = int(mock_type)
            i = 0
            dest_dir_name = flow_path.replace("/", "_")
            scene_name = flow_url_key_value.get("scene_name")
            if scene_name is None:
                scene_name = 'default'
            mock_file_dir = f"/Users/xh/Downloads/ks/lyrebird/mock_json_file/{scene_name}"
            logger.info("mock_file_dir:" + str(mock_file_dir))
            if not os.path.exists(mock_file_dir):
                os.mkdir(mock_file_dir)
            mock_value = flow_url_key_value.get("mock_value")
            if mock_value is None:
                mock_value = 'default'
            if (mock_value.lower() == 'null') or (mock_value.lower() == 'none'):
                mock_value = None
            mock_file_strategy_dir = os.path.join(mock_file_dir, str(mock_value))
            if not os.path.exists(mock_file_strategy_dir):
                os.mkdir(mock_file_strategy_dir)
            if mock_type == -1:
                status_code = int(flow_response['code'])
                if status_code == 200:
                    flow_response['code'] = int(flow_url_key_value.get("mock_status_code")) #更改接口返回状态码为500
                    mock_flow_response=flow_response
                    dest_json_path = os.path.join(mock_file_strategy_dir, f"{dest_dir_name}_{i}_code.json")
                    with open(dest_json_path, 'w', encoding='utf-8') as fw:
                        json.dump(mock_flow_response, fw, indent=4, ensure_ascii=False)
            else:
                if index==0:
                    update_auto_mock_null_robust_config_value('url_key_value', flow_path, 'mock_file_path_li',
                                                              value=[])


                    black_key_list =flow_url_key_value.get("black_key_list")

                    mock_flow_response_dict,get_keys_set=auto_mock_value_by_traverse(origin_data=flow_response,mock_value=mock_value,index=index,black_key_list=black_key_list, mock_type=mock_type)

                    for key in get_keys_set:
                        dest_json_path = os.path.join(mock_file_strategy_dir,f"{dest_dir_name}_{i}_{key}.json")
                        mock_file_path_li.append(dest_json_path)
                        with open(dest_json_path, 'w', encoding='utf-8') as fw:
                            # if data1 != new_li[i]:
                            #     print(f"第{i}次修改成功")
                            # else:
                            #     print(f"第{i}次修改不成功")
                            json.dump(mock_flow_response_dict[i], fw, indent=4, ensure_ascii=False)
                        i = i + 1
                    mock_flow_response = mock_flow_response_dict[index]
                    update_auto_mock_null_robust_config_value('url_key_value', flow_path, 'total_num',
                                                              value=i)
                else:
                    logger.info("mock_file_path_li[index]:"+str(mock_file_path_li[index]))
                    with open(mock_file_path_li[index], 'r', encoding='utf-8') as fw:
                        injson = json.load(fw)
                    mock_flow_response=injson
            if flow_response != mock_flow_response:
                logger.info("数据Mock成功")
                # logger.info("data_json:"+str(data_json))
                # logger.info("copy_data_json:"+str(copy_data_json))
            else:
                logger.info("没有对数据进行Mock")
            logger.info("flow_response:" + str(flow_response))
            logger.info("mock_flow_response:" + str(mock_flow_response))
            # logger.info("mock_flow_response_dict:"+str(mock_flow_response_dict))
            update_auto_mock_null_robust_config_value('url_key_value',flow_path,'mock_file_path_li', value=mock_file_path_li)
            if index>=len(mock_file_path_li):
                index=-1
            update_auto_mock_null_robust_config_value('url_key_value',flow_path,'index', value=(index + 1))

        else:
            logger.info("当前url不在需要Mock的url配置文件中")

    flow['response'] = mock_flow_response





