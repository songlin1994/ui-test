'''
封装执行shell语句方法
'''

import subprocess
from tools.report import log_tool


def invoke(cmd):
    try:
        output, errors = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        o = output.decode("utf-8")
        print(o)
        return o
    except Exception as e:
        log_tool.error('执行命令失败，请检查环境配置')
        log_tool.error(e)
        raise

