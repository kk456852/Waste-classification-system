from django.shortcuts import render, redirect
# 加密算法
import hashlib
# 导入分页插件包
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# 引入模型
from .models import Image, GarbageCategory
from classification_AI.model_load_predict import ProcessAPI


# 调用AI的函数
# 调用模型，图片处理函数
def image_recognize(img):
    recognize_list = ProcessAPI(img.image.url)
    if recognize_list[0] > recognize_list[1]:
        return '不可回收垃圾'


def index(request):
    category = '垃圾种类'
    img = Image.objects.filter(name='default').all()[0]

    if request.method == 'POST':
        file = request.FILES['upload_img']
        image = file
        img = Image.objects.create(image=image)
        # print(img.image.url)
        img.name = img.id
        category_name = image_recognize(img)
        category = GarbageCategory.objects.get(name=category_name)
        img.garbage_category = category
        Image.save(img)
        # category为调用模型返回的结果，下面为暂时的输出值，仅仅输出了图片名字

    return render(request, 'index.html', {
        'category': category,
        'img': img
    })
