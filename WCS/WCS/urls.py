"""WCS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import settings
from django.urls import include
from django.contrib import admin
from django.conf.urls import url
from .settings import MEDIA_ROOT  # 导入项目文件夹中setting中的MEDIA_ROOT绝对路径
from django.views.static import serve
# 引入前端视图文件
from index import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 首页
    url(r'^$', views.index),
    url(r'^index/', views.index),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]
