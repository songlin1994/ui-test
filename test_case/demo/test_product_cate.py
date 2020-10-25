# -*- coding:utf-8 -*-

from time import sleep

import allure

from test_case.business import login_page
from test_case.business import home_page
from test_case.business import product_cate_page
from tools.report import assert_tool

@allure.feature("商品模块")
@allure.story("商品分类")
@allure.title("新增商品分类")
def test_add_product_cate(driver):
    login_page.login(driver)
    home_page.open_product_cate(driver)
    product_cate_page.add_product_cate(driver)
    text = product_cate_page.get_message_text(driver)
    assert_tool.assert_in(text,"成功")
    home_page.close_product_cate(driver)






