from lyrebird import on_request, event
from lyrebird.case_strategy.mock_case_stratergy import *
from util.file_util import get_buried_point_auto_verify_checkers_config_path_value

logger = log.get_logger()




# THRESHOLD_IMG_SIZE: image size limitation



@on_request()
def fixed_value_robust(flow):
    flow_request = flow['request']
    flow_path=flow_request.get('path')
    logger.info("flow_path:" + str(flow_path))
    url_list = get_buried_point_auto_verify_checkers_config_path_value("url_list")
    unwanted_verify_url_list=get_buried_point_auto_verify_checkers_config_path_value("unwanted_verify_url_list")
    logger.info("unwanted_verify_url_list:" + str(unwanted_verify_url_list))
    if len(url_list)==0:
        logger.info("没有需要进行埋点校验的url")
        event.issue("没有需要进行埋点校验的url")
    else:
        if flow_path in url_list:
            logger.info("当前url在需要埋点校验的url配置文件中")
            buried_flag=False
            logger.info("flow_path:"+str(flow_path))
            url_key_value=get_buried_point_auto_verify_checkers_config_path_value("url_key_value")
            flow_url_key_value=url_key_value.get(flow_path)
            if not flow_url_key_value:
                logger.info("buried_point_auto_verify_checkers_config.yaml文件中没有配置当前flow_url的key_value信息，针对当前url无特殊处理逻辑")
            mock_key_value=flow_url_key_value
            for i in range (0,len(mock_key_value)):
                logger.info(f"此时检验{flow_path}中第{i+1}组埋点数据:{[mock_key_value[i]]}")
                flow_request_data=flow_request.get('data')
                logger.info("flow_request_data:"+str(flow_request_data))
                key = list(set((mock_key_value[i])))[0]
                value=mock_key_value[i][key]
                if  key in flow_request_data.keys():
                    logger.info(f"在request中有指定字段{key}，埋点校验字段存在")
                    if value=='xiaoheng_null':
                        logger.info(f"在request中有指定字段{key},不需要校验此字段的值，此字段校验通过")
                        event.issue(f"在{flow_path}中有指定字段{key}，不需要校验此字段的值，此字段校验通过", '')
                        buried_flag=True
                    else:
                        logger.info("value:"+str(value))
                        logger.info("flow_request_data.get(key):"+str(flow_request_data.get(key)))
                        if value==flow_request_data.get(key):
                            logger.info(f"在request中有指定字段{key},需要校验此字段的值，此字段的值校验通过")
                            event.issue(f"在{flow_path}中有指定字段{key}，需要校验此字段的值，值为{value},此字段的值校验通过", '')
                            buried_flag=True
                        else:
                            logger.info(f"在request中有指定字段{key},需要校验此字段的值，此字段的值校验不通过")
                            event.issue(f"在{flow_path}中有指定字段{key}，需要校验此字段的值，值不为{value},此字段的值校验通过", '')
                            buried_flag=False
                    # if buried_flag:
                    #     event.issue(f"在{flow_path}中有指定字段{key}，埋点校验字段存在", '')
                else:
                    logger.info(f"在request中没有指定字段{key}，埋点校验字段不存在")
                    event.issue(f"在{flow_path}中没有指定字段{key}，埋点校验字段不存在",'' )
        else:
            logger.info("当前url不在需要埋点校验的url配置文件中")
    if (unwanted_verify_url_list is None) or (len(unwanted_verify_url_list) == 0):
        logger.info("没有指定的url不需要进行埋点校验")
        event.issue("没有指定的url不需要进行埋点校验",'')
    else:
        if flow_path in unwanted_verify_url_list:
            logger.info("指定的url不需要进行埋点校验不通过，请注意")
            event.issue("指定的url不需要进行埋点校验不通过，请注意",'')
        else:
            logger.info("指定的url不需要进行埋点校验通过，恭喜")
            event.issue("指定的url不需要进行埋点校验通过，恭喜",'')

