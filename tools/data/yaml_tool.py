# -*- coding:utf-8 -*-
# Author : xuepl
# Data ：2019/7/31 22:47
import os

import yaml

from tools.report import log_tool


class YamlTool():

    def __init__(self):
        self.yamls_dict = {}

    def get_yamls(self,dir_path):
        '''
        返回一个所有yaml文件内容的字典
        :param dir_path:yaml文件路径，可以是文件，也可以是文件夹
        :return:
        '''
        self.__get_yamls(dir_path)
        return self.yamls_dict

    def __get_yamls(self,file_path):
        '''
        递归遍历读取文件夹下的yml文件
        :param file_path:
        :return:
        '''
        if os.path.isdir(file_path):
            files = [os.path.join(file_path,f)for f in os.listdir(file_path)]
            for f in files:
                if os.path.isfile(f) and f.endswith(".yml"):
                    self.yamls_dict[os.path.basename(f).split(".")[0]] = self.read_yaml(f)
                elif os.path.isdir(f):
                    self.__get_yamls(f)
        elif os.path.isfile(file_path):
            self.yamls_dict[os.path.basename(file_path).split(".")[0]] = self.read_yaml(file_path)
        else:
            log_tool.error("请输入正确的yaml文件夹")
            raise TypeError("direction is not right")

    def read_yaml(self,yaml_path):
        with open(yaml_path,'r',encoding='utf-8') as f:
            content =yaml.load(f.read(),Loader=yaml.FullLoader)
        return content