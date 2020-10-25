from selenium.common.exceptions import TimeoutException

from tools.report import log_tool


def retry(**kw):
    def wrapper(func):
        def _wrapper(*args,**kwargs):
            raise_ex = None
            for _ in range(kw['retry_num']+1):
                try:
                    return func(*args,**kwargs)
                except TimeoutException as ex:
                    raise_ex = ex
            else:
                log_tool.error("第4次执行失败，程序结束")
                raise raise_ex
        return _wrapper
    return wrapper