#!/usr/bin/env python
# -*- coding: utf-8 -*-

#__title__ = ''
#__author__ = 'xuepl'
#__mtime__ = '2019/9/12'
import random
import re

from tools.data import random_tool
from tools.data.make_info import make_info


en = [chr(i) for i in range(65,91)] + [chr(i) for i in range(97,123)]
num = [ str(i) for i in range(10)]
zf = list(str(bytes([0x60, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2a, 0x2b, 0x2c, 0x2d,
                                  0x2e, 0x2f, 0x3c, 0x3e, 0x3f, 0x40, 0x5b, 0x5c, 0x5d, 0x5e, 0x5f, 0x7b, 0x7c, 0x7d,
                                  0x7e, 0x60])))
zw = [bytes.fromhex(f'{head:x}{body:x}').decode('gb2312') for head in range(0xb0, 0xf7,0x01) for body in range(0xa1, 0xf9,0x01)]
def get_length(s):
    length = 1
    l = s.split(",")
    if (len(l) == 1):
        length = int(l[0])
    elif (len(l) == 2 and (l[0] != '' or l[1] != '')):
        if (l[0] != '' and l[1] != ''):
            length = random.randint(int(l[0]), int(l[1]))

        elif (l[0] == ''):
            length = random.randint(1, int(l[1]))
        else:
            length = random.randint(int(l[0]), 9999)
    else:
        pass
    return length
def get_str(length,ll):
    l = []
    limits = ll[0]
    if (limits.find("字母") != -1):
        l += en
    if (limits.find("数字") != -1):
        l += num
    if (limits.find("特殊字符") != -1):
        l += zf
    if (limits.find("中文") != -1):
        l += zw
    value = ''
    if (len(l) != 0):
        for i in range(length):
            value +=  l[random.randint(0, len(l) - 1)]
    if len(ll) == 2:
        value = ll[1] + value
    return value

def replace_data(s):
    value = ""
    s_l = s.split(" ")
    if(s_l[1].find('字符') != -1 or s_l[1].find('string') != -1):
        s_l[2] = s_l[2].replace('，',',')
        length = get_length(s_l[2])
        value = get_str(length,s_l[3:])
    elif (s_l[1].find("地址") != -1):
        value = random_tool.random_addr()
    elif (s_l[1].find("手机") != -1):
        value = random_tool.random_tell()
    elif (s_l[1].find("邮箱") != -1):
        value = random_tool.random_email()
    elif (s_l[1].find("姓名") != -1):
        value = random_tool.random_name()
    elif (s_l[1].find("数字") != -1):
        s_l[2] = s_l[2].replace('，', ',')
        value = get_length(s_l[2])
    elif (s_l[1].find("身份证") != -1):
        value = make_info()["身份证号"]
    else:
        value = None
    return value


def get_json_data(dic,pa,d):
    for key in pa:
        path = pa[key].strip()
        if(not path.startswith("$")):
            print("请输入正确的jsonpath")
            return
        p_list = path.split('.')
        n_list = []
        for p in p_list:
            if (p.find('[') != -1):
                start = p.index('[')
                end = p.index(']')
                n_list.append(p[:start])
                n_list.append(p[start+1:end])
                try:
                    if(p[end+1:] != ''):
                        n_list.append(p[end+1:])
                except:
                    pass
            else:
                n_list.append(p)

        for i in n_list[1:]:
            if(i.isdigit()):
                dic=dic[int(i)]
            else:
                dic = dic[i]
        d[key] = dic

def replace_str(s,data):
    r = re.compile(r"\${(.*?)}")
    s_l = r.findall(s)
    for l in s_l:
        s = s.replace("${"+l+"}",data[l])
    return s


def index_dic(d,data):
    if(isinstance(d,dict)):
        for key in d:
            if (isinstance(d[key], str)):
                try:
                    d[key] = replace_str(d[key],data)
                except:
                    pass
                if (d[key].find("自动生成") != -1):
                    d[key] = replace_data(d[key].strip())
            else:
                index_dic(d[key],data)
    elif(isinstance(d,list)):
        for i in range(len(d)):
            if (isinstance(d[i], str)):
                d[i] = d[i].strip()
                if(d[i].startswith("$") and d[i].endswith("}")):
                    try:
                        d[i] = data[d[i][2:-1]]
                    except:
                        pass
                if (d[i].startswith("自动生成")):
                    d[i] = replace_data(d[i])
            else:
                index_dic(d[i], data)
    else:
        pass
    return d

if __name__ == '__main__':
     data = {"token":"sssssss"}
     s = "fff${token}${token}ddd"
     s = replace_str(s,data)
     print(s)