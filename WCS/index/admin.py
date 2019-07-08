from django.contrib import admin
from .models import Image, GarbageCategory

# Register your models here.

admin.site.register(Image)
admin.site.register(GarbageCategory)
