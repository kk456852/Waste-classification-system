from keras.models import load_model
from classification_AI.load_data import load_pic

# 初始化Django的同时加载模型而不是每调用一次加载一次否则报错
# 参考：https://www.cnblogs.com/yanjj/p/8242595.html
# 参考：https://zhuanlan.zhihu.com/p/27101000
# 参考：https://blog.csdn.net/Cyril__Li/article/details/79054596
print('load model...')
model = load_model("classification_AI/model.h5")
print('load done')
data = load_pic("media/images/hello.jpg")
print('test model...')
test_result = model.predict([[data]])
print('test done')
