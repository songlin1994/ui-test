# -*- coding:utf-8 -*-
import allure
import pytest

from config.config import TEST_CASE
from tools.ui.base_ui import BaseUI
from tools.ui.get_pages import Pages


'''
debug 启动浏览器命令
chrome.exe --remote-debugging-port=9111 --user-data-dir="d:\selenium\data"
'''

@pytest.fixture(scope='session')
def driver():
    pages = Pages(TEST_CASE)
    # pages.start_browser("chrome") # 正常模式
    # pages.start_browser("chrome_debugger") # debug模式
    pages.start_browser("chrome_headless")  # 无头模式
    yield pages
    pages.quit()

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    '''
    用例失败截图
    :param item:
    :param call:
    :return:
    '''
    # 获取钩子方法的调用结果
    out = yield
    # print('用例执行结果', out)
    # 3. 从钩子方法的调用结果中获取测试报告
    report = out.get_result()
    if report.when == "call" and report.outcome == "failed":
        page = Pages(TEST_CASE)
        with allure.step(page.element_dir + "操作失败"):
            allure.attach(page.screenshot_as_png(),"操作失败",allure.attachment_type.PNG)

