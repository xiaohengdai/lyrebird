import copy
import random
import json
from lyrebird import on_response, log


logger = log.get_logger()


duplicate_li = []  # 表示所有节点的key(包含有子节点的节点)，去重li
key_list = []
# 修改指定key的value值，包含在response中的key里的key
def check_json_value(dic_json, k, v,mock_type=0):
    '''
    dic_json:原始json数据
    k:
    v:
    mock_type:mock模式，0代表指定值，1代表根据数据类型的随机值，2代表文件名后缀替换（图片、视频），
    3代表某个key是否存在（与模式0逻辑一致）,在yaml文件中配置指定值时，均定为-99999
    '''
    if isinstance(dic_json, dict):
        for key in list(dic_json.keys()):
            duplicate_li.append(key)
            if key == k:
                # logger.info("dic_json:" + str(dic_json))
                # logger.info("k:" + str(k))
                # logger.info("v:" + str(v))
                if mock_type==0:
                    dic_json[key] = v
                elif mock_type==1:
                    dic_json[key] = get_random_value_by_datatype(v)           #在这里加根据数据类型随机mock策略
                elif mock_type==2:
                    dic_json[key] =get_file_type_value(dic_json[key])           #根据文件格式名后缀Mock
                elif mock_type==3:
                    if 'ImmutableMultiDict' not in str(type(dic_json)):
                        dic_json[key] = v
                    else:
                        logger.info("ImmutableMultiDict和dic_json:" + str(dic_json))
                elif mock_type==4:
                    dic_json[key] =get_empty_value_by_datatype(v)   #根据不同数据类型赋为不同空值
                elif mock_type==5:
                    logger.info("dic_json:"+str(dic_json))
                    dic_json.pop(k)
            elif isinstance(dic_json[key], dict):
                check_json_value(dic_json[key], k, v,mock_type)
            elif isinstance(dic_json[key], list):
                if key==k:
                    dic_json[key] = v
                else:
                    for i in range(0, len(dic_json[key])):
                        check_json_value(dic_json[key][i], k, v,mock_type)
            # else:
            #     logger.info("key1:"+str(key))
    # logger.info("dic_json:"+str(dic_json))

# coding:utf-8



def get_dict_allkeys(dict_a):
    """
    遍历嵌套字典，获取json返回结果的所有key值
    :param dict_a:
    :return: key_list
    """
    if isinstance(dict_a, dict):  # 使用isinstance检测数据类型
        # 如果为字典类型，则提取key存放到key_list中
        for x in range(len(dict_a)):
            temp_key = list(dict_a.keys())[x]
            temp_value = dict_a[temp_key]
            key_list.append(temp_key)
            get_dict_allkeys(temp_value)  # 自我调用实现无限遍历
    elif isinstance(dict_a, list):
        # 如果为列表类型，则遍历列表里的元素，将字典类型的按照上面的方法提取key
        for k in dict_a:
            if isinstance(k, dict):
                for x in range(len(k)):
                    temp_key = list(k.keys())[x]
                    temp_value = k[temp_key]
                    key_list.append(temp_key)
                    get_dict_allkeys(temp_value) # 自我调用实现无限遍历
    return key_list




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
    li_set = set(duplicate_li)
    # logger.info("duplicate_li:" + str(duplicate_li))
    # print('li_set:', li_set)

    # 获取去重后的节点个数
    node_num_unrepeat = len(li_set)
    # # print("node_num_unrepeat:", node_num_unrepeat)
    # node_list_num_unrepeat = list(li_set)

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

def get_empty_value_by_datatype(origin_value):
    empty_value=''
    if isinstance(origin_value, str):
        empty_value = ''
    elif isinstance(origin_value, int):
        empty_value=0
    elif isinstance(origin_value, list):
        empty_value = []
    elif isinstance(origin_value,dict):
        empty_value={}
    return empty_value







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


def auto_mock_value_by_traverse(origin_data,mock_value=None,index=0,black_key_list=[], mock_type=0):
    get_keys = get_dict_allkeys(origin_data)
    get_keys = set(get_keys) #得到的集合顺序可能不一致，导致每次遍历生成的结果不尽相同
    get_keys=get_keys-set(black_key_list)  #去除黑名单中需要遍历的Key
    get_keys=list(get_keys)
    get_keys.sort()  #对遍历的key排序，保证每次遍历生成的Mock文件一致
    # print("get_keys:",get_keys)
    print("len(get_keys):", len(get_keys))
    new_li = {}
    i = 0
    for key in get_keys:
        # key='isOriginal'  #测试具体某个key
        copy_data = copy.deepcopy(origin_data)
        # print(f"第{i}个{key}")
        # if i==index:
        #
        #     logger.info(f"第{i}个key:{key}")
        logger.info("auto_mock_value_by_traverse中key:" + str(key))
        check_json_value(copy_data, key, mock_value, mock_type=mock_type)
        # if i==index:
        #     print("copy_data:",copy_data)
        new_li[i] = copy_data
        i = i + 1
    return new_li,get_keys



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
    # data1={
    # "liveStreamCount": 0,
    # "contactsUploaded": True,
    # "avatarUploaded": True,
    # "pcursor": "no_more",
    # "llsid": "2000388741504046066",
    # "phoneBinded": True,
    # "host-name": "bjpg-rs1576.yz02",
    # "qqFriendsUploaded": True,
    # "result": 1,
    # "hasMoreLiveStream": False,
    # "feeds": [],
    # "new_notify": 0,
    # "needShowInterestedUser": True
    # }

    # k='rawText'
    # v='*@!#$%^我1s?:8'
    # check_json_value(dic_json, k, v)
    # print("dic_json:",dic_json)
    # data = """{}"""
    # data1 = json.loads(dic_json)
    path = "/Users/xh/Downloads/ks/lyrebird/lyrebird/examples/checkers/test.json"
    # 读取文件数据
    with open(path, "r") as f:
        data1 = json.load(f)
    # print("data1:",data1)

    new_li,get_keys_set=auto_mock_value_by_traverse(data1,mock_value=None,index=11)

    # print("new_li[1]:", new_li[1])
    i=0
    mock_file_path_li=[]
    for key in get_keys_set:
        dest_json_path=f"/Users/xh/Downloads/ks/lyrebird/lyrebird/examples/checkers/res_{i}_{key}.json"
        mock_file_path_li.append(dest_json_path)
        with open(dest_json_path, 'w', encoding='utf-8') as fw:
            if data1 != new_li[i]:
                print(f"第{i}次修改成功")
            else:
                print(f"第{i}次修改不成功")
            json.dump(new_li[i], fw, indent=4, ensure_ascii=False)
        i=i+1
    # print("type(new_li):",type(new_li))
    # print("len(new_li):",len(new_li))
    # # print("new_li:",new_li)
    # logger.info("new_li:"+str(new_li))

    # copy_data = copy.deepcopy(data1)
    # check_json_value(copy_data, 'isOriginal', None, mock_type=0)
    # print("copy_data:",copy_data)
    with open(mock_file_path_li[0], 'r', encoding='utf-8') as fw:
        injson = json.load(fw)
        print("injson:",injson)


