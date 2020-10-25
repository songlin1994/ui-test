import allure

from tools.data.random_tool import random_string


@allure.step("添加商品分类页面")
def add_product_cate(driver):
    driver.click("商品分类.添加按钮")
    driver.send_keys("新增商品分类.分类名称输入框",random_string("abcdefghigklmnopqrst1234567",7))
    driver.click("新增商品分类.上级分类下拉框")
    driver.click(["新增商品分类.上级分类下拉选项","服装"])
    driver.send_keys("新增商品分类.数量单位输入框", random_string("abcdefghigklmnopqrst1234567", 7))
    driver.send_keys("新增商品分类.排序输入框", random_string("01", 1))
    driver.click(["新增商品分类.是否显示单选框","是"])
    driver.click(["新增商品分类.是否显示在导航栏单选框","是"])
    driver.click(["新增商品分类.筛选属性下拉框",1])
    driver.click(["新增商品分类.一级属性选项",1,"服装-T恤"])
    driver.click(["新增商品分类.二级属性选项",1,"商品编号"])
    driver.send_keys("新增商品分类.关键词输入框", random_string("abcdefghigklmnopqrst1234567",7))
    driver.send_keys("新增商品分类.分类描述输入框", random_string("abcdefghigklmnopqrst1234567",7))
    driver.click("新增商品分类.提交按钮")
    driver.click(["新增商品分类.确认提示","确定"])

@allure.step("获取消息提示框文本")
def get_message_text(driver):
    return driver.get_text("新增商品分类.操作结果提示框")