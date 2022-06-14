import os,shutil,json

from lyrebird.case_strategy.mock_case_stratergy import check_json_value

mock_inspector_dir_data_path="/Users/xh/.lyrebird/mock_data/personal/.lyrebird_prop"
ext = os.path.splitext(mock_inspector_dir_data_path)  # 将文件名路径与后缀名分开
# print("ext:", ext)
dst_file = ext[0] + '_copy.json'
shutil.copyfile(mock_inspector_dir_data_path, dst_file)


mock_inspector_dir_data_json={}
with open(dst_file, 'r', encoding='utf-8') as fw:
    mock_inspector_dir_data_json = json.load(fw)
# print("mock_inspector_dir_data_json:",mock_inspector_dir_data_json)


social_mock_git_data='/Users/xh/Downloads/ks_beifen/socialmockdata'

check_json_value(mock_inspector_dir_data_json,k='name',v=-1,mock_type=-2)

# def process_child_data(children,parent_dir_path):
#     if children is not None:
#         for j in range (0,len(children)):
#             parent_dir_name = children[j]['name'] #Todo:这里其实可以为多个
#             parent_dir_path = os.path.join(parent_dir_path, parent_dir_name)
#             print("parent_dir_name:", parent_dir_name)
#             if not os.path.exists(parent_dir_path):
#                 os.mkdir(parent_dir_path)
#             children=children[j].get('children')
#     return children,parent_dir_path
#
#
# children=mock_inspector_dir_data_json['children']
# parent_dir_path=social_mock_git_data
# children,parent_dir_path = process_child_data(children, parent_dir_path)
# children=children.get('children')
# children,parent_dir_path = process_child_data(children, parent_dir_path)
# children=children.get('children')
# children,parent_dir_path = process_child_data(children, parent_dir_path)
# children = children.get('children')
# children,parent_dir_path=process_child_data(children,parent_dir_path)
# children = children.get('children')
# process_child_data(children,parent_dir_path)



