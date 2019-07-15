from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.sessions.models import Session

# 加密算法
import hashlib
# 导入分页插件包
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# 引入模型
from .models import Image, GarbageCategory, GoodsCategory, Users
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
    if request.method == 'POST':
        if request.session.get('username', default=None):
            # 获取前端传入的文件,并在图片数据库中创建词条
            file = request.FILES['upload_img']
            image = file
            img = Image.objects.create(image=image)
            if img:
                # print(img.image.url)
                img.name = img.id
                print(img.name)

                # 调用AI图像识别函数
                good_category_name = image_recognize(img)

                # 保存数据库
                good_category = GoodsCategory.objects.get(name=good_category_name)
                # good_category = GoodsCategory.objects.get(name='未知')
                garbage_category = good_category.garbage_category.name
                img.goods_category = good_category
                Image.save(img)
                good = img

                # web前端输出：
                # good_category = good_category.name
                # garbage_category = garbage_category.name
                print(garbage_category)
                if garbage_category == '可循环物':
                    return render(request, 'recycled_detail.html',
                                  {
                                      'good': good,
                                  })
                elif garbage_category == '有害垃圾':
                    return render(request, 'hazardous_detail.html',
                                  {
                                      'good': good,
                                  })
                elif garbage_category == '其他垃圾':
                    return render(request, 'other_detail.html',
                                  {
                                      'good': good,
                                  })
                elif garbage_category == '厨余垃圾':
                    return render(request, 'kitchen_detail.html',
                                  {
                                      'good': good,
                                  })
        else:
            return render(request, 'prompt.html')

    return render(request, 'index.html')


def garbage_detail(request):
    id = request.GET.get('id')
    print(id)
    good = Image.objects.get(id=id)
    garbage_category = good.goods_category.garbage_category.name
    if garbage_category == '可循环物':
        render(request, 'recycled_detail.html',
               {
                   'good': good,
               })
    elif garbage_category == '有害垃圾':
        render(request, 'hazardous_detail.html',
               {
                   'good': good,
               })
    elif garbage_category == '其他垃圾':
        render(request, 'other_detail.html',
               {
                   'good': good,
               })
    elif garbage_category == '厨余垃圾':
        render(request, 'kitchen_detail.html',
               {
                   'good': good,
               })


def hazardous_detail(request):
    return render(request, 'hazardous_detail.html')


def kitchen_detail(request):
    return render(request, 'kitchen_detail.html')


def other_detail(request):
    return render(request, 'other_detail.html')


def recycled_detail(request):
    return render(request, 'recycled_detail.html')


def index_text(request):
    if request.method == 'POST':
        # 获取前端传入的文件,并在图片数据库中创建词条
        name = request.POST.get("good", None)
        if GoodsCategory.objects.filter(name=name).exists():
            good = GoodsCategory.objects.get(name=name)
            garbage_category = good.garbage_category.name
            if garbage_category == '可循环物':
                return render(request, 'recycled_detail_text.html',
                              {
                                  'name': name,
                              })
            elif garbage_category == '有害垃圾':
                return render(request, 'hazardous_detail_text.html',
                              {
                                  'name': name,
                              })
            elif garbage_category == '其他垃圾':
                return render(request, 'other_detail_text.html',
                              {
                                  'name': name,
                              })
            elif garbage_category == '厨余垃圾':
                return render(request, 'kitchen_detail_text.html',
                              {
                                  'name': name,
                              })
        else:
            return render(request, 'garbage_tips_none.html')

    return render(request, 'index_text.html')


def garbage_tips(request):
    return render(request, 'garbage_tips.html')


def prompt(request):
    return render(request, 'prompt.html')


def sign_out(request):
    if request.method == 'POST':
        try:
            del request.session['username']
            return redirect('/sign_in/')
        except KeyError:
            pass
    return render(request, 'sign_out.html')


def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get("username")  # 按name获取
        password = request.POST.get("password")

        sha256 = hashlib.sha256(bytes('加一些东西', encoding='utf-8') + b'zqacm')
        sha256.update(bytes(password, encoding='utf-8'))
        password = sha256.hexdigest()

        # 查询
        ret = Users.objects.filter(username=username, password=password)
        # print(ret)
        # print(type(ret))
        if ret:
            # 登录之前，先把用户名记录下来
            request.session['username'] = username
            return redirect('/index/')

    return render(request, 'sign_in.html')


def sign_up(request):
    # 接收前端数据保存到数据库
    if request.method == 'POST':
        # print('POST_hello')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_again = request.POST.get('password_again')

        # 查询
        ret = Users.objects.filter(username=username)
        # print(ret)
        # print(type(ret))

        # 该逻辑需要优化
        if ret.exists():
            return HttpResponse("用户名已经存在")

        # 存到数据库
        if username and password and password == password_again:
            # 缺少头像
            sha256 = hashlib.sha256(bytes('加一些东西', encoding='utf-8') + b'zqacm')
            sha256.update(bytes(password, encoding='utf-8'))
            password = sha256.hexdigest()
            ret = Users.objects.create(username=username, password=password)
            if ret:
                # 成功了
                return redirect('/sign_in/')
        else:
            return redirect('/sign_up/')

    return render(request, 'sign_up.html')
