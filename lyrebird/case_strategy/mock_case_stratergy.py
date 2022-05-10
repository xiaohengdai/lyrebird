import copy
import random

from lyrebird import on_response, log


logger = log.get_logger()

li = []  # 表示所有节点的key(包含有子节点的节点)

# 修改指定key的value值，包含在response中的key里的key
def check_json_value(dic_json, k, v,mock_type=0):
    '''
    dic_json:原始json数据
    k:
    v:
    mock_type:mock模式，0代表指定值，1代表根据数据类型的随机值，2代表文件名后缀替换（图片、视频）
    '''
    if isinstance(dic_json, dict):
        for key in dic_json:
            li.append(key)
            if key == k:
                # logger.info("dic_json:" + str(dic_json))
                # logger.info("k:" + str(k))
                # logger.info("v:" + str(v))
                if mock_type==0:
                    dic_json[key] = v
                elif mock_type==1:
                    dic_json[key] = get_random_value_by_datatype(v)           #在这里加根据数据类型随机mock策略
                elif mock_type==2:
                    dic_json[key] =get_file_type_value(dic_json[key])   #根据文件格式名后缀Mock
            elif isinstance(dic_json[key], dict):
                check_json_value(dic_json[key], k, v,mock_type)
            elif isinstance(dic_json[key], list):
                for i in range(0, len(dic_json[key])):
                    check_json_value(dic_json[key][i], k, v,mock_type)
            # else:
            #     logger.info("key1:"+str(key))
    # logger.info("dic_json:"+str(dic_json))


def set_per_key_value(data_json,mock_key_value,mock_type=0):#mock_key_value是个列表
    copy_data_json = copy.deepcopy(data_json)
    # 获取各个子节点

    for i in range (0,len(mock_key_value)):
        one_mock_key_value=mock_key_value[i]
        logger.info("one_mock_key_value:"+str(one_mock_key_value))
        one_mock_key=list(set(one_mock_key_value))[0]
        logger.info("one_mock_key:"+one_mock_key)
        one_mock_value=one_mock_key_value[one_mock_key]
        logger.info("one_mock_value:"+str(one_mock_value))
        check_json_value(copy_data_json, one_mock_key,one_mock_value,mock_type=mock_type)
    # 针对接口中带用户名的将其改为固定值
    # 对子节点列表去重
    li_set = set(li)
    # logger.info("li:" + str(li))
    # print('li_set:', li_set)

    # 获取去重后的节点个数
    node_num_unrepeat = len(li_set)
    # print("node_num_unrepeat:", node_num_unrepeat)
    node_list_num_unrepeat = list(li_set)

    logger.info("data_json==copy_data_json:"+str((data_json==copy_data_json)))

    return copy_data_json
    # 依次将去重后的每个子节点设为null
    # for j in range(0, 1):
    #     logger.info("开始设置")
    #     copy_data_json = copy.deepcopy(data_json)
    #     logger.info("对字段" + node_list_num_unrepeat[j] + "进行修改")
    #     check_json_value(copy_data_json, node_list_num_unrepeat[j], 'null')
    #     logger.info("copy_data_json:", copy_data_json)
    #     flow_response = copy_data_json

def get_random_value_by_datatype(origin_value):
    # user_name_mock='*@!#$%^我1s?:'#字符串的
    # descriptio_name_mock='*@!#$%^我1s?:8'#字符串的
    # rawText_mock='*@!#$%^我1s?:8'#字符串的
    # id_mock=1*20  #整型的
    # playInfo_mock={}  #字典
    # users_mock=[]  #列表
    random_value=''
    random_value_len=4
    if isinstance(origin_value, str):
        logger.info("value是字符串类型，采用字符串随机值进行mock")
        random_value = 'a'*random.randint(1, 10 ** random_value_len)
    elif isinstance(origin_value, int):
        logger.info("value是int类型，采用整型随机值进行mock")
        random_value=random.randint(1,10**random_value_len)
    elif isinstance(origin_value, list):
        logger.info("value是list类型，采用列表随机值进行mock")
        if len(origin_value)>0:
            random_value = origin_value[0]*random.randint(1, 10 ** random_value_len)
            # random_value = origin_value[0] * random.randint(1, 1)
        else:
            random_value = ['a'] * random.randint(1, 10 ** random_value_len)

    return random_value


def get_specific_file_type_value(type_list,origin_value):
    new_value = origin_value
    is_exist=False
    for i in range(0, len(type_list)):
        if type_list[i] in origin_value:
            original_file_type = type_list[i]
            type_list.remove(original_file_type)
            index = random.randint(0, len(type_list) - 1)
            logger.info("index:" + str(index))
            new_value = origin_value.replace(original_file_type, type_list[index])
            is_exist=True
            break
    return new_value,is_exist

def get_file_type_value(origin_value):
    pic_type_list=['.png','.jpg','.heif']
    #heif:“使用HEIF格式的图片，一般文件名的后缀为.HEIC（还有其他不常见后缀格式），它所带来的直接好处就是在保证图像质量的前提下，将照片的文件体积减小了50%.”
    video_type_list=['.mp4','.avi','.wmv']
    new_value,is_exist0= get_specific_file_type_value(pic_type_list,origin_value)
    if not is_exist0:
        new_value,is_exist1 = get_specific_file_type_value(video_type_list, origin_value)
        if is_exist1:
            logger.info("对视频格式后缀做替换")
        else:
            logger.info("origin_value:"+str(origin_value))
            logger.info("没有匹配的图片、视频格式后缀")
    # else:
    #     logger.info("对图片格式后缀做替换")
    return new_value



# def get_random_mock_value(mock_key_value):
#     for i in range (0,len(mock_key_value)):
#         one_mock_key_value=mock_key_value[i]
#         logger.info("one_mock_key_value:"+str(one_mock_key_value))
#         one_mock_key=list(set(one_mock_key_value))[0]
#         logger.info("one_mock_key:"+one_mock_key)
#         one_mock_value=one_mock_key_value[one_mock_key]
#         logger.info("one_mock_value:"+str(one_mock_value))
#         one_mock_value=get_random_value(one_mock_value)
#         #还需要回传到mock_key_value中
#         list(set(mock_key_value[i]))[0]=one_mock_value
#     logger.info("mock_key_value:"+str(mock_key_value))
#     mock_key_random_value=mock_key_value
#     return mock_key_random_value


if __name__ == '__main__':
    dic_json={"a":{'rawText': '你可能认识的人'}, 'rawText': {'relation_common_count': 0, 'relation_text_id': 44921}, 'userCount': 0, 'scene': 0, 'pageType': 0, 'title': None}
    k='rawText'
    v='*@!#$%^我1s?:8'
    check_json_value(dic_json, k, v)
    print("dic_json:",dic_json)