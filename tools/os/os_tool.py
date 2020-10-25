# -*- coding:utf-8 -*-
# Author : 小吴老师
# Data ：2019/7/11 18:31
import os
import shutil
import stat


def get_root_path():
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)).replace('\\', '/')
    print(root_path)
    if root_path.find('venv') > 0:
        root_path=root_path[:root_path.find('venv')-1]
    return root_path+'/'

def deldir(dir):
    if os.path.exists(dir):
        for file in os.listdir(dir):
            file = os.path.join(dir, file)
            if os.path.isdir(file):
                print("remove dir", file)
                os.chmod(file, stat.S_IWRITE|stat.S_IWOTH)
                deldir(file)
            elif os.path.isfile(file) :
                print("remove file", file)
                os.chmod(file, stat.S_IWRITE|stat.S_IWOTH)
                os.remove(file)
        shutil.rmtree(dir,True)

def mkdir(path):
    is_exists = os.path.exists(path)
    if not is_exists:
        os.makedirs(path)

def remove(path):
    is_exists = os.path.exists(path)
    if is_exists:
        os.remove(path)

def exists(file_or_path):
    is_exists = os.path.exists(file_or_path)
    return is_exists
#
# def copy_dir(source_path,target_path):
#     if not os.path.exists(target_path):
#         os.makedirs(target_path)
#
#     if os.path.exists(source_path):
#         # root 所指的是当前正在遍历的这个文件夹的本身的地址
#         # dirs 是一个 list，内容是该文件夹中所有的目录的名字(不包括子目录)
#         # files 同样是 list, 内容是该文件夹中所有的文件(不包括子目录)
#         for root, dirs, files in os.walk(source_path):
#             for file in files:
#                 src_file = os.path.join(root, file)
#                 shutil.copy(src_file, target_path)
#                 print(src_file)
#
#     print('copy files finished!')

def move(src_dir,target_dir):
    if not os.path.exists(target_dir):
        shutil.move(src_dir,target_dir)

def copy_dir(src_dir,target_dir):
    if not os.path.exists(target_dir):
        shutil.copytree(src_dir,target_dir)

def copy_file(src_file,target_dir):
    shutil.copy(src_file,target_dir)