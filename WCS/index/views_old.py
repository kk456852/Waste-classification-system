from django.shortcuts import render, redirect
# 加密算法
import hashlib
# 导入分页插件包
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# 引入模型
from .models import Image, GarbageCategory, GoodsCategory
from classification_AI.model_load_predict import ProcessAPI

goods = {
    0: '硬纸板',
    1: '玻璃制品',
    2: '易拉罐',
    3: '纸片',
    4: '塑料瓶',
    5: '包装袋',
}


# 调用AI的函数
# 调用模型，图片处理函数
def image_recognize(img):
    recognize_list = ProcessAPI(img.image.url[1:])
    recognize_list = recognize_list.tolist()
    i = recognize_list[0].index(max(recognize_list[0]))
    print(goods[i])
    return goods[i]


def index(request):
    garbage_category = '垃圾种类'
    good_category = '物品种类'
    img = Image.objects.filter(name='default').all()[0]

    if request.method == 'POST':
        # 获取前端传入的文件,并在图片数据库中创建词条
        file = request.FILES['upload_img']
        image = file
        img = Image.objects.create(image=image)
        # print(img.image.url)
        img.name = img.id

        # 调用AI图像识别函数
        good_category_name = image_recognize(img)

        # 保存数据库
        good_category = GoodsCategory.objects.get(name=good_category_name)
        # good_category = GoodsCategory.objects.get(name='未知')
        garbage_category = good_category.garbage_category
        img.goods_category = good_category
        Image.save(img)

        # web前端输出：
        good_category = good_category.name
        garbage_category = garbage_category.name

    return render(request, 'index_old.html', {
        'garbage_category': garbage_category,
        'good_category': good_category,
        'img': img
    })
