

from tools.data.yaml_tool import  YamlTool
from tools.report import log_tool


# 自定义元类，用于实现单例模式
from tools.ui.base_ui import BaseUI



class Pages(BaseUI):

    def __init__(self,dir_path,timeout=10):
        '''
        :param dir_path: 文件或文件夹路径
        '''
        super().__init__(timeout)
        yml_tool = YamlTool()
        self.pages = yml_tool.get_yamls(dir_path) # 获取页面对象

    def get_locator(self, element_dir):
        '''
        获取某个页面的locator
        :param element_dir: 元素路径
        :return:
        '''

        if isinstance(element_dir,str):
            self.element_dir = element_dir
            p, el_name = element_dir.split('.')
            page = self.get_page(p)
            if el_name not in page:
                log_tool.error("{}页面中不存在{}".format(p, el_name))
                raise NameError("{} is not in {}".format(el_name, p))
            localtor = page[el_name]
        else:
            self.element_dir = element_dir[0]
            p,el_name = self.element_dir.split('.')
            page = self.get_page(p)
            if el_name not in page:
                log_tool.error("{}页面中不存在{}".format(p,el_name))
                raise NameError("{} is not in {}".format(el_name,p))
            else:
                localtor = page[el_name]
            # 解决定位语句参数化问题
            if len(element_dir) > 1:
                localtor = page[el_name].format(*element_dir[1:])
        self.shot("定位元素", element_dir, " 定位语句为：", localtor.strip())
        return super().get_locator(localtor.strip())

    def get_page(self,page_name):
        '''
        获取页面元素对象
        :param page_name:页面名称（yaml文件名）
        :return:
        '''
        if page_name in self.pages:
            return self.pages[page_name]
        log_tool.error("找不到{}页面".format(page_name))
        raise NameError("{} not find".format(page_name))






if __name__ == '__main__':
    p = Pages("../../test_case")
    print(p.pages)
    print(p.get_locator("百度首页.搜索框","kw"))
