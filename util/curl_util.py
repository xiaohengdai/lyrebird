import curlify
import requests,json
from lyrebird import log

logger = log.get_logger()

def get_curl_request_by_flow(flow_request):
    method=flow_request['method']
    logger.info("method:"+str(method))
    print("method:",method)
    headers=flow_request['headers']
    print("headers:", headers)
    logger.info("headers:" + str(headers))
    data=flow_request['data']
    print("data:", data)
    logger.info("data:" + str(data))
    url=flow_request['url']
    print("url:", url)
    logger.info("url:" + str(url))

    response = requests.request(method, url, headers=headers, data=data)
    print("response.text:",response.text)

    curl_request=curlify.to_curl(response.request, compressed=True)
    print("curl_request:",curl_request)
    logger.info("******")
    logger.info("curl_request:"+str(curl_request))
    logger.info("******")

def get_curl_request_by_json(json_path):
    # 读取文件数据
    with open(json_path, "r") as f:
        data1 = json.load(f)
    print("data1:",data1)
    get_curl_request_by_flow(data1)



if __name__ == '__main__':
    json_path='/Users/xh/Downloads/ks/lyrebird/lyrebird/examples/checkers/test.json'
    get_curl_request_by_json(json_path)






