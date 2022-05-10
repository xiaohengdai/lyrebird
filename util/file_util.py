import yaml,os


project_dir=os.path.abspath(os.path.join(os.getcwd(), '..'))
print("project_dir:",project_dir)
if 'lyrebird' not in project_dir:
    project_dir=os.path.join(project_dir, 'lyrebird')
checkers_conf_path = os.path.join(project_dir, 'lyrebird','examples', 'checkers','checkers_config.yaml')
print("checkers_conf_path:",checkers_conf_path)
random_by_datatype_checkers_config_path= os.path.join(project_dir, 'lyrebird','examples', 'checkers','random_by_datatype_checkers_config.yaml')
file_type_replace_robust_checkers_config_path=os.path.join(project_dir, 'lyrebird','examples', 'checkers','file_type_replace_robust_checkers_config.yaml')

def get_yaml(file_path):
    with open(file_path, encoding='utf-8') as f:
        try:
            y_instance = yaml.load(f, Loader=yaml.SafeLoader)
            return y_instance
        except yaml.YAMLError as e:
            print(e)


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


if __name__ == '__main__':
    url_list=get_checkers_config_value("url_list")
    print("url_list:",url_list)