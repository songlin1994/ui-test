# -*- coding:utf-8 -*-
# Data ：2019/7/10 6:26

import configparser
import os


class ConfigTool:

    def __init__(self):
        root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)).replace('\\','/')
        file_path = '/config/config.ini'
        file_name = root_path + file_path
        print(file_name)
        self.config = configparser.ConfigParser()
        print(file_name)
        self.config.read(file_name)

    def get_conf(self,section,option):
        return self.config.get(section,option)


    def get_api_url(self,section):
        protocal = self.get_conf(section, 'protocal')
        host = self.get_conf(section, 'host')
        port = self.get_conf(section, 'port')

        url = protocal + '://' + host + ':' + port
        return url

    def get_db_dict(self,section):
        db_dict = dict()
        db_dict['host'] = self.get_conf(section, 'host')
        db_dict['port'] = int(self.get_conf(section, 'port'))
        db_dict['db'] = self.get_conf(section, 'db')
        db_dict['user'] = self.get_conf(section, 'user')
        db_dict['passwd'] = self.get_conf(section, 'passwd')
        db_dict['charset'] = self.get_conf(section, 'charset')
        print(type(db_dict))
        print(db_dict)
        return  db_dict
