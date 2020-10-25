import allure


@allure.step("登录页面登录")
def login(driver):
    driver.get("http://mall.yansl.com/#/login")
    driver.send_keys("登录页面.用户名输入框","admin")
    driver.send_keys("登录页面.密码输入框","123456")
    driver.click("登录页面.登录按钮")