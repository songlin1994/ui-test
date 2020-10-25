
# 自定义元类，用于实现单例模式
class SingLeton(type):

    def __init__(cls, *args, **kwargs):
        super(SingLeton, cls).__init__(*args, **kwargs)
        cls.instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__call__(*args, **kwargs)
        return cls.instance