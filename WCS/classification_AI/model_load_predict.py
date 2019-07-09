from .load_data import load_pic
# 引用初始化时加载的全局变量model
from WCS.__init__ import model


def ProcessAPI(pic_path):
    data = load_pic(pic_path)
    test_result = model.predict([[data]])
    return test_result
