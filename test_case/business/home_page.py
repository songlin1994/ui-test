import allure


@allure.step("打开商品分类页面")
def open_product_cate(driver):
    driver.click("商城首页.商品菜单")
    driver.click("商城首页.商品分类菜单")

@allure.step("返回首页")
def close_product_cate(driver):
    driver.click("商城首页.商品菜单")
    driver.click("商城首页.首页菜单")
