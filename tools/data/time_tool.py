# -*- coding:utf-8 -*-
# Data ：2019/7/31 21:47
import datetime

def get_now():
    date_time=str(datetime.datetime.now())[0:19]
    print(date_time)
    return date_time

def get_today():
    date=str(datetime.datetime.now())[0:10]
    print(date)
    return date

def get_time():
    time = str(datetime.datetime.now())[11:19]
    print(time)
    return time

if __name__ == '__main__':
    get_now()
    get_today()
    get_time()
