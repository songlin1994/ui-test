# -*- coding:utf-8 -*-
from tools.report import log_tool
from tools.os import shell_tool
import pytest

if __name__ == '__main__':
    # 修改成要执行的测试用例
    test_case = './test_case/demo'

    xml_report_path = './allure-results/'
    html_report_path = './reports/html/'

    pytest.main(['-s', '-q', '--alluredir',
                 xml_report_path, test_case])
    # cmd1 = 'allure generate %s -o %s --clean' % (xml_report_path, html_report_path)
    #
    # shell_tool.invoke(cmd1)


