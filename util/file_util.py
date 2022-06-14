import yaml,os


project_dir=os.path.abspath(os.path.join(os.getcwd(), '..'))
print("project_dir:",project_dir)
if 'lyrebird' not in project_dir:
    project_dir=os.path.join(project_dir, 'lyrebird')
checkers_conf_path = os.path.join(project_dir, 'lyrebird','examples', 'checkers','checkers_config.yaml')
print("checkers_conf_path:",checkers_conf_path)
random_by_datatype_checkers_config_path= os.path.join(project_dir, 'lyrebird','examples', 'checkers','random_by_datatype_checkers_config.yaml')
file_type_replace_robust_checkers_config_path=os.path.join(project_dir, 'lyrebird','examples', 'checkers','file_type_replace_robust_checkers_config.yaml')
buried_point_auto_verify_checkers_config_path=os.path.join(project_dir,'lyrebird','examples','checkers','buried_point_auto_verify_checkers_config.yaml')
auto_mock_null_robust_config_path=os.path.join(project_dir,'lyrebird','examples','checkers','auto_mock_null_robust_config.yaml')

def get_yaml(file_path):
    with open(file_path, encoding='utf-8') as f:
        y_instance = yaml.load(f, Loader=yaml.SafeLoader)
        return y_instance


def update_auto_mock_null_robust_config_value(*args, value=None) -> str:
    """
    更新yaml中key对应的value
    :param args: 对应的key值
    :param value:
    """
    obj = get_yaml(auto_mock_null_robust_config_path)
    tmp = obj

    for arg in args[:-1]:
        tmp = tmp[arg]

    tmp[args[-1]] = value
    # print('update config: key:{}, value:{}'.format(str(args), value))
    with open(auto_mock_null_robust_config_path, encoding='utf-8', mode='w') as fw:
        yaml.dump(obj, fw, sort_keys=False, allow_unicode=True)

def get_config_value(*args,file_path) -> str:
    """
    在yaml中根据key获取对应的value
    :param args: 对应的key值
    :return:
    """
    obj = get_yaml(file_path)
    print("obj:",obj)
    for arg in args:
        print("arg:",arg)
        obj = obj.get(arg) if arg else None
    return obj


def get_checkers_config_value(*args) -> str:
    """
    在yaml中根据key获取对应的value
    :param args: 对应的key值
    :return:
    """
    obj = get_yaml(checkers_conf_path)
    for arg in args:
        obj = obj.get(arg) if arg else None
    return obj

def get_auto_mock_null_robust_config_value(*args) -> str:
    """
    在yaml中根据key获取对应的value
    :param args: 对应的key值
    :return:
    """
    obj = get_yaml(auto_mock_null_robust_config_path)
    print("obj:",obj)
    for arg in args:
        print("arg:",arg)
        obj = obj.get(arg) if arg else None
    return obj

def get_random_checkers_config_value(*args) -> str:
    """
    在yaml中根据key获取对应的value
    :param args: 对应的key值
    :return:
    """
    obj = get_yaml(random_by_datatype_checkers_config_path)
    for arg in args:
        obj = obj.get(arg) if arg else None
    return obj

def get_file_type_replace_robust_checkers_config_path_value(*args) -> str:
    """
    在yaml中根据key获取对应的value
    :param args: 对应的key值
    :return:
    """
    obj = get_yaml(file_type_replace_robust_checkers_config_path)
    for arg in args:
        obj = obj.get(arg) if arg else None
    return obj

def get_buried_point_auto_verify_checkers_config_path_value(*args):
    """
        在yaml中根据key获取对应的value
        :param args: 对应的key值
        :return:
        """
    obj = get_yaml(buried_point_auto_verify_checkers_config_path)
    for arg in args:
        obj = obj.get(arg) if arg else None
    return obj


if __name__ == '__main__':
    # url_list=get_checkers_config_value("url_list")
    # print("url_list:",url_list)
    # update_auto_mock_null_robust_config_value('url_key_value','/rest/n/user/recommend/v3','mock_value', value=None)
    # update_auto_mock_null_robust_config_value('url_key_value','/rest/n/user/recommend/v3','index', value= 1)
    # url_list = get_auto_mock_null_robust_config_value("url_list")
    # print(url_list)
    url_list =get_config_value("url_list",file_path="/Users/xh/Downloads/ks/lyrebird/lyrebird/examples/checkers/亲密关系个人落地页.yaml")
    print(url_list)