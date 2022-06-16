# -*- coding:utf-8 -*-
# Data ：2019/7/31 8:26

# 字典转字符串
def dic_to_str(dic):
    s = ''
    for key in dic:
        s+="{0}: {1}\n".format(key,dic[key])
    return s
