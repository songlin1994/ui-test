# coding=utf-8
import os

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

from config.config import DRIVER_PATH, BROWSER_PATH
from tools.report import log_tool
from tools.report.retry_tool import retry
from tools.security.type_tool import SingLeton

retry_num = 3 # 失败重试次数
class BaseUI(metaclass=SingLeton):

    original_window = None
    def __init__(self,timeout=10):
        self.driver=None
        '''

        :param timeout: 显式、隐式等待超时时间
        '''
        self.timeout = timeout
        self.location_type_dict = {
            "xpath": By.XPATH,
            "id": By.ID,
            "name": By.NAME,
            "css_selector": By.CSS_SELECTOR,
            "class_name": By.CLASS_NAME,
            "tag_name": By.TAG_NAME,
            "link_text": By.LINK_TEXT,
            "partial_link_text": By.PARTIAL_LINK_TEXT
        }

    def start_browser(self ,browser='chrome'):

        '''
        启动浏览器
        :param browser: 浏览器类型
        '''
        if self.driver:
            log_tool.info("浏览器以启动，请勿再次启动浏览器。")
            return self
        try:
            if browser == "firefox" or browser == "ff":
                self.driver = webdriver.Firefox()
            elif browser == "chrome":
                chrome_options = Options()
                chrome_options.binary_location = BROWSER_PATH
                # chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
                self.driver = webdriver.Chrome(executable_path = DRIVER_PATH,options=chrome_options)
                self.driver.maximize_window()
                self.wait_time()
            elif browser == "internet explorer" or browser == "ie":
                self.driver = webdriver.Ie()
            elif browser == "opera":
                self.driver = webdriver.Opera()
            elif browser == "chrome_headless":
                chrome_options = Options()
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--disable-gpu')
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument("--window-size=1920,1080")
                chrome_options.binary_location = BROWSER_PATH
                # chrome_options.add_experimental_option('excludeSwitches',['enable-automation'])
                self.driver = webdriver.Chrome(executable_path = DRIVER_PATH,options=chrome_options)
                self.wait_time()
            elif browser == "chrome_debugger":
                print("chrome_debugger模式")
                chrome_options = Options()
                chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9111")
                chrome_options.binary_location=BROWSER_PATH
                # chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
                self.driver = webdriver.Chrome(executable_path = DRIVER_PATH, options=chrome_options)
                self.driver.maximize_window()
                self.wait_time()
            elif browser == 'edge':
                self.driver = webdriver.Edge()
            else:
                log_tool.error("启动浏览器失败，没有找到%s浏览器，请输入'ie', 'ff', 'opera', 'edge', 'chrome' or 'chrome_headless'"% browser)
                raise NameError(
                    "启动浏览器失败，没有找到%s浏览器，请输入'ie', 'ff', 'opera', 'edge', 'chrome' or 'chrome_headless'"% browser)
        except WebDriverException:
            log_tool.error("启动浏览器失败,请检查webdriver是否配置，或者webdriver版本是否和浏览器匹配")
            raise
        self.shot("-------测试开始，启动{}浏览器成功-------".format(browser))

    def get_locator(self, locator):
        '''
        解析定位关键字
        :param locator:定位语句 例如：xpath=>//*[@id='kw']
        :return: 元组(By.XPATH,"//*[@id='kw']")
        '''

        if "=>" not in locator and "xpath" not in locator:
            by = "xpath"
            value = locator
        elif("=>" in locator):
            by = locator.split("=>")[0].strip()
            value = locator.split("=>")[1].strip()
            if by not in (self.location_type_dict):
                log_tool.error("%s中的定位方式错误，请输入正确的定位方式:"
                                "id,name,class_name,xpath,tag_name,css_selector,link_text,partial_link_text"%(locator))
                raise TypeError("%s中的定位方式错误，请输入正确的定位方式:"
                                "id,name,class_name,xpath,tag_name,css_selector,link_text,partial_link_text"%(locator))
            if by == "" or value == "":
                log_tool.error("%s格式错误，定位方式=>值 示例：'id=>useranme'"%(locator))
                raise NameError("%s格式错误，定位方式=>值 示例：'id=>useranme'"%(locator))
        else:
            log_tool.error("%s格式错误，定位方式=>值 示例：'id=>useranme'" % (locator))
            raise NameError("%s格式错误，定位方式=>值 示例：'id=>useranme'"%(locator))
        return (self.location_type_dict[by],value)

    def get_element(self,locator):
        '''
        根据传入的数据来定位页面元素
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :return: 元素定位结果
        '''

        try:
            return self.wait_util_visibility(locator)
        except TimeoutException:
            time_out_error = "{}定位元素超时，请检查定为语句是否正确，或者尝试其他定位方式".format(locator)
            log_tool.error(time_out_error)
            raise TimeoutException(time_out_error)

    def shot(self,*args, **kwargs):
        message = ""
        for i in range(len(args)):
            message += "{} "
        log_tool.info(message.format(*args))



    def max_window(self):
        '''
        最大化浏览器
        :return:
        '''
        self.shot("最大化浏览器")
        self.driver.maximize_window()

    def set_window(self, wide, high):
        '''
        设置浏览器大小
        :param wide: 宽
        :param high: 高
        :return:
        '''
        self.shot("设置浏览器大小,宽：",wide,"高",high)
        self.driver.set_window_size(wide, high)

    def close(self):
        '''
        关闭浏览器，不退出driver
        :return:
        '''
        self.shot("关闭浏览器，不退出driver")
        self.driver.close()

    def quit(self):
        '''
        关闭浏览器并退出driver
        :return:
        '''
        self.shot("关闭浏览器并退出driver")
        self.driver.quit()

    @retry(retry_num=retry_num)
    def get(self, url):
        '''
        打开网址
        :param url:网址
        :return:
        '''
        self.shot("打开网址：",url)
        self.driver.get(url)


    def forward(self):
        '''
        前进
        :return:
        '''
        self.shot("前进")
        self.driver.forward()


    def back(self):
        '''
        后退
        :return:
        '''
        self.shot("后退")
        self.driver.back()


    def refresh(self):
        '''
        刷新
        :return:
        '''
        self.shot("刷新")
        self.driver.refresh()

    def get_title(self):
        '''
        获取当前页面的title
        :return: title
        '''
        self.shot("获取当前页面的title:",self.driver.title)
        return self.driver.title

    def get_url(self):
        '''
        获取当前页面的网址
        :return: url
        '''
        self.shot("获取当前页面的url",self.driver.current_url)
        return self.driver.current_url

    @retry(retry_num=retry_num)
    def send_keys(self, locator, text):
        '''
        先清空文本(clear)输入框，再输入(send_keys)内容
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :param text: 输入的文本内容
        :return:
        '''

        element = self.get_element(locator)
        self.shot(self.element_dir,"中输入：", text)
        ActionChains(self.driver).click(element).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(
            Keys.BACKSPACE).perform()

        element.send_keys(text)

    @retry(retry_num=retry_num)
    def click(self, locator):
        '''
        左键单击操作
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :return:
        '''

        element = self.get_element(locator)
        self.shot("点击",self.element_dir)
        ActionChains(self.driver).move_to_element(element).click(element).perform()

    @retry(retry_num=retry_num)
    def click_by_js(self, locator):
        '''
        #通过xpath执行js代码点击元素
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :return:
        '''
        try:
            el = self.get_element(locator)
            loc = self.get_locator(locator)
            self.shot("使用js代码点击",self.element_dir)
            if (loc[0] == self.location_type_dict["xpath"]):
                js = "var xpath = \"" + self.double_to_single_mark(
                loc[1]) + "\";var element = document.evaluate(xpath,document,null,XPathResult.ANY_TYPE,null).iterateNext();element.click();"
                self.execute_script(js)
            else:
                message = "元素点击失败，请使用xpath定位，例如：xpath=>//*[@id='kw']"
                log_tool.error(message)
                raise TypeError(message)
        except:
            log_tool.error("点击元素失败:" +self.element_dir+ " 定位语句为："+locator)
            raise

    @retry(retry_num=retry_num)
    def right_click(self, locator):
        '''
        右键单击操作
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :return:
        '''
        el = self.get_element(locator)
        self.shot("右击",self.element_dir)
        ActionChains(self.driver).context_click(el).perform()

    @retry(retry_num=retry_num)
    def double_click(self, locator):
        '''
        左键双击操作
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :return:
        '''
        el = self.get_element(locator)
        self.shot("双击",self.element_dir)
        ActionChains(self.driver).double_click(el).perform()

    @retry(retry_num=retry_num)
    def move_to_element(self, locator):
        '''
        鼠标移动到元素上方，并保持悬浮
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :return:
        '''
        el = self.get_element(locator)
        self.shot("鼠标悬浮在",self.element_dir,"上")
        ActionChains(self.driver).move_to_element(el).perform()

    @retry(retry_num=retry_num)
    def drag_and_drop(self, el_locator, ta_locator):
        '''
        拖拽一个元素到另一个元素
        :param el_locator: 要拖拽的元素，定位语句 例如：xpath=>//*[@id='kw']
        :param ta_locator: 拖拽的目标元素，定位语句 例如：xpath=>//*[@id='kw']
        :return:
        '''
        element = self.get_element(el_locator)
        el_name = self.element_dir
        target = self.get_element(ta_locator)
        ta_name = self.element_dir
        self.shot("拖拽：",el_name," 至： ",ta_name)
        ActionChains(self.driver).drag_and_drop(element, target).perform()

    @retry(retry_num=retry_num)
    def drag_and_drop_by_offset(self, locator, x, y):
        '''
        拖拽元素移动一定距离
        :param locator: 要拖拽的元素，定位语句 例如：xpath=>//*[@id='kw']
        :param x: 屏幕横向移动的距离，往右为正，往左为负
        :param y: 屏幕纵向移动的距离，往下为正，往上为负
        :return:
        '''
        element = self.get_element(locator)
        self.shot("拖拽：",self.element_dir,"横向移动：", x,"像素,纵向移动",y,'像素')
        ActionChains(self.driver).drag_and_drop_by_offset(element, x, y).perform()

    @retry(retry_num=retry_num)
    def submit(self, locator):
        '''
        对元素执行表单提交操作
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :return:
        '''
        el = self.get_element(locator)
        self.shot("提交表单",self.element_dir)
        el.submit()

    @retry(retry_num=retry_num)
    def scroll_screen_x_y(self,x,y):
        '''
        滚动窗口横向滚动x像素，纵向滚动y像素， 往右x为正值，左x为负值，下y为正值，上y为负值
        :param x:屏幕横向滚动的距离，单位像素 往右x为正值，左x为负值
        :param y:屏幕纵向滚动的距离，单位像素 下y为正值，上y为负值
        :return:
        '''
        self.shot("屏幕横向滚动：", x, "像素",'纵向滚动:',y,'像素')
        js = "window.scrollBy({},{})".format(x,y)
        self.driver.execute_script(js)

    @retry(retry_num=retry_num)
    def scroll_screen_to_element(self,locator):
        '''
        滚动窗口至元素locator出现
        :param locator: 要拖拽的元素，定位语句 例如：xpath=>//*[@id='kw']
        :return:
        '''
        el = self.get_element(locator)
        self.shot("屏幕滚动至元素：",self.element_dir,'出现')
        js = "arguments[0].scrollIntoView();"
        self.driver.execute_script(js,el)

    @retry(retry_num=retry_num)
    def execute_script(self, script):
        '''
        执行js代码
        :param script:
        :return:
        '''
        self.shot("执行js代码：", script)
        self.driver.execute_script(script)

    @retry(retry_num=retry_num)
    def get_attribute(self, locator, attribute):
        '''
        获取元素属性的值
        :param locator:定位语句 例如：xpath=>//*[@id='kw']
        :param attribute: 属性名
        :return: 属性值
        '''
        el = self.get_element(locator)
        value = el.get_attribute(attribute)
        self.shot("获取元素：",self.element_dir,' 属性: ',attribute," 的值为: ",value)
        return value

    @retry(retry_num=retry_num)
    def get_text(self, locator):
        '''
        获取元素展示文本
        :param locator:定位语句 例如：xpath=>//*[@id='kw']
        :return: 展示文本
        '''
        el = self.get_element(locator)
        text = el.text
        self.shot("获取元素：", self.element_dir, " 的展示文本为: ", text)
        return text

    @retry(retry_num=retry_num)
    def get_page_source(self):
        page_source = self.driver.page_source
        self.shot( "获取页面源代码")
        return page_source

    @retry(retry_num=retry_num)
    def is_display(self, locator):
        '''
        判断元素是否可见
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :return: 可见为true 不可见为false
        '''
        el = self.get_element(locator)
        display = el.is_displayed()
        if display:
            self.shot("元素：", self.element_dir, " 可见 ")
        else:
            self.shot("元素：", self.element_dir, " 不可见 ")
        return display

    def double_to_single_mark(self, s):
        '''
        将字符串中的双引号转换成单引号
        :param s: 字符串
        :return: 字符串
        '''
        return s.replace('"', '\'')

    @retry(retry_num=retry_num)
    def update_attribute_by_xpath(self,locator,attribute_name,attribute_value):
        '''
        #通过xpath根据修改html标签属性的值
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :param attribute_name:属性名
        :param attribute_value: 属性值
        :return:
        '''
        try:
            el = self.get_element(locator)
            loc = self.get_locator(locator)
            self.shot("修改元素：",self.element_dir,'属性:',attribute_name,'的值为：',attribute_value)
            if (loc[0] == self.location_type_dict["xpath"]):
                js = "var xpath = \"" + self.double_to_single_mark(
                    loc[1]) + "\";var element = document.evaluate(xpath,document,null,XPathResult.ANY_TYPE,null).iterateNext();element.setAttribute(\"" + attribute_name + "\",\"" + attribute_value + "\");"
                self.execute_script(js)
            else:
                message = "修改元素：{} 属性的值失败，请使用xpath定位，示例：xpath=>//*[@id='kw']"
                log_tool.error(message)
                raise TypeError(message)
        except:
            log_tool.error("修改属性值失败，属性名:" + attribute_name + " 属性值:" + attribute_value)
            raise

    @retry(retry_num=retry_num)
    def remove_attribute_by_xpath(self,locator,attribute_name):
        '''
        #通过xpath删除html标签属性
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :param attribute_name:属性名
        :return:
        '''
        try:
            el = self.get_element(locator)
            loc = self.get_locator(locator)
            self.shot("删除元素：", self.element_dir, '的', attribute_name,'属性:')
            if (loc[0] == self.location_type_dict["xpath"]):
                js = "var xpath = \"" + self.double_to_single_mark(
                    loc[1]) + "\";var element = document.evaluate(xpath,document,null,XPathResult.ANY_TYPE,null).iterateNext();element.removeAttribute(\"" + attribute_name + "\");"
                self.execute_script(js)
        except:
            print("修改属性值失败，属性名:" + attribute_name)
            raise

    # @retry(retry_num=retry_num)
    # def file_upload(self,locator,file_path):
    #     '''
    #     点击上传文件按钮并上传文件
    #     :param locator: 定位语句 例如：xpath=>//*[@id='kw']
    #     :param file_path: 文件路径
    #     :return:
    #     '''
    #     self.click(locator)
    #     autoit.win_wait("打开", 10)
    #     self.sleep(1)
    #     file_path = os.path.abspath(file_path)
    #     self.shot("上传文件",file_path)
    #     # autoit.control_send("打开", "Edit1", os.path.abspath(file_path))
    #     autoit.control_set_text("打开", "Edit1", file_path)
    #     autoit.control_click("打开", "Button1")

    @retry(retry_num=retry_num)
    def get_alert_text(self):
        '''
        获取弹框的展示文本
        :return:展示文本
        '''
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.alert_is_present)
        except:
            log_tool.error("切换弹窗失败，当前页面不存在弹窗")
            raise
        text = self.driver.switch_to.alert.text
        self.shot("获取弹框展示文本为：",text)
        return text

    @retry(retry_num=retry_num)
    def alert_send_keys(self,text):
        '''
        #窗口切换至弹窗输入内容并确定
        :param text: 输入的文本
        :return:
        '''

        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.alert_is_present)
        except:
            log_tool.error("切换弹窗失败，当前页面不存在弹窗")
            raise

        alert = self.driver.switch_to.alert
        self.shot("弹框输入：",text)
        alert.send_keys(text)

    @retry(retry_num=retry_num)
    def alert_accept(self):
        '''
        切换到弹框并确认
        :return:
        '''
        try:
            alert = WebDriverWait(self.driver, 5, 0.5).until(EC.alert_is_present)
            alert.accept()
        except:
            log_tool.error("切换弹窗失败，当前页面不存在弹窗")
            raise
        self.shot("弹框确定操作")

    @retry(retry_num=retry_num)
    def alert_dismiss(self):
        '''
        切换至弹框，并取消
        :return:
        '''
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.alert_is_present)
        except:
            log_tool.error("切换弹窗失败，当前页面不存在弹窗")
            raise
        self.shot("弹框取消操作")
        self.driver.switch_to.alert.dismiss()

    @retry(retry_num=retry_num)
    def switch_to_frame(self, locator):
        '''
        切入iframe框架里边
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :return:
        '''
        iframe_el = self.get_element(locator)
        self.shot("切入iframe：",self.element_dir)
        self.driver.switch_to.frame(iframe_el)


    def switch_to_current_frame_out(self):
        '''
        退出当前iframe
        :return:
        '''
        self.shot("退出当前iframe")
        self.driver.switch_to.parent_frame()

    def switch_to_frame_out(self):
        '''
        切出iframe,回到主界面
        :return:
        '''
        self.shot("切出iframe，回到主界面")
        self.driver.switch_to.default_content()

    @retry(retry_num=retry_num)
    def switch_to_windows_by_title(self, title):
        '''
        #切换到名字为title的窗口
        :param title: 窗口标题
        :return: 返回值：当前窗口的句柄
        '''
        self.shot("切换窗口至：",title)
        current = self.driver.current_window_handle
        handles = self.driver.window_handles
        for handle in handles:
            self.driver.switch_to.window(handle)
            if (self.driver.title.__contains__(title)):
                break
        return current


    def screenshot_as_file(self, file_path):
        '''
        截图
        :param file_path: 文件路径
        :return:
        '''
        self.shot("截图，图片保存地址为:", file_path)
        self.driver.get_screenshot_as_file(file_path)


    def screenshot_as_png(self):
        '''
        截图
        :return:
        '''
        self.shot("截图，png图片")
        return self.driver.get_screenshot_as_png()

    @retry(retry_num=retry_num)
    def select_by_value(self, locator, value):
        '''
        操作select标签，根据标签的value属性值选择
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :param value: select标签value属性的值
        :return:
        '''
        el = self.get_element(locator)
        self.shot("选择value值为：",value,' 的选项')
        Select(el).select_by_value(value)

    @retry(retry_num=retry_num)
    def select_by_index(self, locator, value):
        '''
        操作select标签，根据选项的下标选择，下标从0开始
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :param value: 选项的下标
        :return:
        '''
        el = self.get_element(locator)
        self.shot("选择第", value + 1, ' 个选项')
        Select(el).select_by_index(value)

    @retry(retry_num=retry_num)
    def select_by_text(self, locator, value):
        '''
        操作select标签，根据选项的展示文本选择
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :param value: 下拉选项的展示文本
        :return:
        '''
        el = self.get_element(locator)
        self.shot("选择文本为:", value  ,' 的选项')
        Select(el).select_by_visible_text(value)

    def sleep(self, sec):
        '''
        线程休眠
        :param sec: 秒数
        :return:
        '''
        time.sleep(sec)

    def wait_time(self):
        '''
        元素定位的隐式等待
        :param secs: 最长秒数
        :return:
        '''
        self.driver.implicitly_wait(self.timeout)

    @retry(retry_num=retry_num)
    def wait_util_presence(self,locator,secs=10):
        '''
        显示等待页面元素出现在DOM中，但并不一定可见，存在则返回该页面元素对象
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :param secs: 最长等待时间
        :return:元素对象
        '''
        locator = self.get_locator(locator)
        try:
            element = WebDriverWait(self.driver, secs).until(
                        EC.presence_of_element_located(locator))
            return element
        except Exception as e:
            raise e


    def wait_util_visibility(self, locator, secs=10):
        '''
        显示等待页面元素的出现，并返回元素对象
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :param secs: 最长等待时间
        :return:元素对象
        '''
        locator = self.get_locator(locator)
        try:
            element = WebDriverWait(self.driver, secs).until(
                EC.visibility_of_element_located(locator))
            return element
        except Exception as e:
            raise e

    @retry(retry_num=retry_num)
    def wait_util_not_visibility(self, locator, secs=10):
        '''
        显示等待页面元素不可见
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :param secs: 最长等待时间
        :return:
        '''
        locator = self.get_locator(locator)
        try:
            WebDriverWait(self.driver, secs).until(
                EC.invisibility_of_element_located(locator))

        except Exception as e:
            raise e

    @retry(retry_num=retry_num)
    def wait_util_clickable(self, locator, secs=10):
        '''
        判断某个元素中是否可见并且是可点击的，并返回元素对象
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :param secs: 等待超时时间
        :return:元素对象
        '''
        locator = self.get_locator(locator)
        try:
            element = WebDriverWait(self.driver, secs).until(
                EC.element_to_be_clickable(locator))
            return element
        except Exception as e:
            raise e

    @retry(retry_num=retry_num)
    def wait_util_selected(self, locator, secs=10):
        '''
        判断某个元素是否被选中了,一般用在select下拉框
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :param secs: 等待超时时间
        :return:
        '''
        locator = self.get_locator(locator)
        try:
            element = WebDriverWait(self.driver, secs).until(
                EC.element_to_be_selected(locator))
            return element
        except Exception as e:
            raise e

    @retry(retry_num=retry_num)
    def wait_util_text(self, locator,text, secs=10):
        '''
        判断text是否存在于元素展示文本中
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :param text: 判断内容
        :param secs: 等待超时时间
        :return: 存在返回：true 不存在返回：flase
        '''
        locator = self.get_locator(locator)
        try:
            is_true = WebDriverWait(self.driver, secs).until(
                EC.text_to_be_present_in_element(locator,text))
            return is_true
        except Exception as e:
            raise e

    @retry(retry_num=retry_num)
    def wait_util_at_lest_one(self,locator, secs=10):
        '''
        判断是否至少有1个元素存在于dom树中，如果定位到就返回列表
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :param secs: 等待超时时间
        :return: 定位到的元素对象列表
        '''
        locator = self.get_locator(locator)
        try:
            items = WebDriverWait(self.driver, secs).until(
                EC.presence_of_all_elements_located(locator))
            return items
        except Exception as e:
            raise e

    @retry(retry_num=retry_num)
    def wait_util_title_is(self,title, secs=10):
        '''
        判断页面标题和title相等
        :param title: 指定标题内容
        :param secs: 等待超时时间
        :return: 相等返回：true 不相等返回：false
        '''
        try:
            is_true = WebDriverWait(self.driver, secs).until(
                EC.title_is(title))
            return is_true
        except Exception as e:
            raise e

    @retry(retry_num=retry_num)
    def wait_util_title_contains(self, title, secs=10):
        '''
        显示等待页面title包含指定内容
        :param title: 标题指定内容
        :param secs: 等待超时时间
        :return: 包含返回：true，不包含返回：false
        '''
        try:
            is_true = WebDriverWait(self.driver, secs).until(
                EC.title_contains(title))
            return is_true
        except Exception as e:
            raise e

    @retry(retry_num=retry_num)
    def wait_util_alert_present(self, secs=10):
        '''
        判断页面上是否存在alert,如果有就切换到alert
        :param secs: 等待超时时间
        :return: 弹框对象
        '''
        try:
            return WebDriverWait(self.driver, secs).until(
                EC.alert_is_present())
        except Exception as e:
            raise e

    @retry(retry_num=retry_num)
    def wait_util_frame_available(self, locator, secs=10):
        '''
        检查frame是否存在，存在则切换进去
        :param locator:定位语句 例如：xpath=>//*[@id='kw']
        :param secs: 等待超时时间
        :return:
        '''
        locator = self.get_locator(locator)
        try:
            WebDriverWait(self.driver, secs).until(
                EC.frame_to_be_available_and_switch_to_it(locator))
        except Exception as e:
            raise e