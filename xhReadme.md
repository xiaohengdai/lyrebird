lyrebird启动命令:
/Users/xh/Downloads/ks/lyrebird/venv_lyrebird/bin/python3 -m lyrebird --script /Users/xh/Downloads/ks/lyrebird/lyrebird/examples/checkers/buried_point_auto_verify.py --log /Users/xh/Downloads/ks/lyrebird/log/mock_log.log --data /Users/xh/Downloads/ks_beifen/socialmockdata/mock_data/personal

/Users/xh/Downloads/ks/lyrebird/venv_lyrebird/bin/python3 -m lyrebird --script /Users/xh/Downloads/ks/lyrebird/lyrebird/examples/checkers/auto_mock_null_robust.py --log /Users/xh/Downloads/ks/lyrebird/log/mock_log.log --data /Users/xh/Downloads/ks_beifen/socialmockdata/mock_data/personal

/Users/xh/Downloads/ks/lyrebird/venv_lyrebird/bin/python3 -m lyrebird --script /Users/xh/Downloads/ks/lyrebird/lyrebird/examples/checkers/auto_mock_null_robust.py --data /Users/xh/Downloads/ks_beifen/socialmockdata/mock_data/personal

/Users/xh/Downloads/ks/lyrebird/venv_lyrebird/bin/python3 -m lyrebird --data /Users/xh/Downloads/ks_beifen/socialmockdata/mock_data/personal
*脚本录制:
/Users/xh/Downloads/ks/lyrebird/venv_lyrebird/bin/python3 -m lyrebird --script /Users/xh/Downloads/ks/lyrebird/lyrebird/examples/checkers/record.py --log /Users/xh/Downloads/ks/lyrebird/log/mock_log.log --data /Users/xh/Downloads/ks_beifen/socialmockdata/mock_data/personal

截图:
tidevice screenshot /Users/xh/Downloads/ks/lyrebird/screenshot.jpg


Python深度遍历查找字典键对应的值，在多层嵌套的字典中找到你要的数据：https://blog.csdn.net/qq_26373925/article/details/105073790


mac安装pycurl:
https://github.com/transloadit/python-sdk/issues/4
pycurl==7.43.0 --global-option=build_ext --global-option="-L/usr/local/opt/openssl/lib" --global-option="-I/usr/local/opt/openssl/include"

Mock策略：
mock_type: -1 #修改状态码为500  mock_value: status_code
mock_type: 0   #置null  mock_value:null
mock_type: 4   #置空 mock_value:empty
mock_type: 5  #删除某个key  mock_value: delete_key


