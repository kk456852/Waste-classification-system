from django.contrib import admin
from .models import Image, GarbageCategory, GoodsCategory

# Register your models here.

admin.site.register(Image)
admin.site.register(GarbageCategory)
admin.site.register(GoodsCategory)
