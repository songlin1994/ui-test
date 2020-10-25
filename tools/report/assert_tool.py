'''
封装Assert方法

'''
from tools.report import log_tool
import json


def assert_in(body, expected_msg):
    '''
    验证response body中是否包含预期字符串
    :param body:
    :param expected_msg:
    :return:
    '''
    try:
        text = json.dumps(body, ensure_ascii=False)
        # print(text)
        assert expected_msg in text
        return True

    except:
        log_tool.error("不包含期望值, 期望值 是  %s" % expected_msg)
        raise


def assert_equal(body, expected_msg):
    '''
    验证response body中是否等于预期字符串
    :param body:
    :param expected_msg:
    :return:
    '''
    try:
        assert body == expected_msg
        return True
    except:
        log_tool.error("Response body != expected_msg, expected_msg is %s, body is %s" % (expected_msg, body))
        raise


def assert_time(time, expected_time):
    '''
    验证response body响应时间小于预期最大响应时间,单位：毫秒
    :param body:
    :param expected_time:
    :return:
    '''
    try:
        assert time < expected_time
        return True

    except:
        log_tool.error("Response time > expected_time, expected_time is %s, time is %s" % (expected_time, time))
        raise


def assert_not_null(actual):
    '''
            验证实际结果不为null
            :param actual:
            :return:
            '''
    try:
        assert actual != ''
        return True

    except:
        log_tool.error("预期不为空，实际结果为空")
        raise
