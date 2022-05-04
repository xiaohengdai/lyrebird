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
from lyrebird import on_response

mock_flow_response = ""


# THRESHOLD_IMG_SIZE: image size limitation


# @event('flow')
# def robust_test(msg):

#     #aprint("msg:",msg)
#     # 1.ignore unexepcted object
#     if ignore_check(msg):
#         return
#     # 2.prepare useful info

#     flow_response=msg['flow']['response']
#     # print("type(flow_response):",type(flow_response))
#     # print("flow_response:",flow_response)
#     # 3.check data
#     #set_per_key_value(flow_response)
#     mock_flow_response=copy.deepcopy(flow_response)
#     check_json_value(mock_flow_response, 'displayName', '生成海报')
#     print("执行robust_test方法")
#     # print("mock_flow_response:",mock_flow_response)
#     #flow.response.set_text(mock_flow_response)
#     title = 'robust set success \n'

#     description = 'robust set success\n'

#     event.issue(title, description)

def ignore_check(msg):
    if 'name' in msg.keys():
        if msg['name'] != 'server.response':
            return True
        if 'response' not in msg['flow']:
            return True
        if 'image' not in msg['flow']['response']['headers']['Content-Type']:
            return True
    return False


li = []  # 表示所有节点的key(包含有子节点的节点)


# 修改指定key的value值
def check_json_value(dic_json, k, v):
    if isinstance(dic_json, dict):
        for key in dic_json:
            li.append(key)
            if key == k:
                dic_json[key] = v
            elif isinstance(dic_json[key], dict):
                check_json_value(dic_json[key], k, v)
            elif isinstance(dic_json[key], list):
                for i in range(0, len(dic_json[key])):
                    check_json_value(dic_json[key][i], k, v)


def set_per_key_value(data_json, flow_response):
    copy_data_json = copy.deepcopy(data_json)
    # 获取各个子节点
    check_json_value(copy_data_json, 'id', '13333333333')

    # 对子节点列表去重
    li_set = set(li)
    # print('li_set:', li_set)

    # 获取去重后的节点个数
    node_num_unrepeat = len(li_set)
    # print("node_num_unrepeat:", node_num_unrepeat)
    node_list_num_unrepeat = list(li_set)

    # 依次将去重后的每个子节点设为null
    for j in range(0, 1):
        print("开始设置")
        copy_data_json = copy.deepcopy(data_json)
        print("对字段" + node_list_num_unrepeat[j] + "进行修改")
        check_json_value(copy_data_json, node_list_num_unrepeat[j], 'null')
        print("copy_data_json:", copy_data_json)
        flow_response = copy_data_json


# @on_response()
# def change_assign_response(flow):#针对指定的url进行指定的规则进行Mock

#     # print('mock_flow_response1:',mock_flow_response)
#     print("type(flow['response']):",type(flow['response']))

#     flow_response=flow['response']
#     mock_flow_response=copy.deepcopy(flow_response)
#     check_json_value(mock_flow_response, 'displayName', None)
#     check_json_value(mock_flow_response, 'iconUrl', None)
#     flow['response']=mock_flow_response
#     print("flow['response']:",flow['response'])

@on_response()
def change_all_key_response(flow):
    # print('mock_flow_response1:',mock_flow_response)
    print("type(flow['response']):", type(flow['response']))

    flow_response = flow['response']

    mock_flow_response = copy.deepcopy(flow_response)
    set_per_key_value(mock_flow_response, flow_response)
    # check_json_value(mock_flow_response, 'displayName', None)
    # check_json_value(mock_flow_response, 'iconUrl', None)
    # flow['response']=mock_flow_response
    # print("flow['response']:",flow['response'])


