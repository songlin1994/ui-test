# -*- coding:utf-8 -*-
# Author : 小吴老师
# Data ：2019/7/31 18:56

import zipfile
import os


# zipfile解压
def unzip_file(zipfilename, unziptodir):
    if not os.path.exists(unziptodir): os.mkdir(unziptodir)
    zfobj = zipfile.ZipFile(zipfilename)
    for name in zfobj.namelist():
        name = name.replace('\\', '/')
        if name.endswith('/'):
            os.mkdir(os.path.join(unziptodir, name))
        else:
            ext_filename = os.path.join(unziptodir, name)
            ext_dir = os.path.dirname(ext_filename)
            if not os.path.exists(ext_dir): os.mkdir(ext_dir)
            outfile = open(ext_filename, 'wb')
            outfile.write(zfobj.read(name))
            outfile.close()


if __name__ == '__main__':
    unzip_file('C:/softwareData/PycharmProjects/test-ui-1/chrom_driver/chromedriver_win32.zip',
               'C:/softwareData/PycharmProjects/test-ui-1/chrom_driver')
