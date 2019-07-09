from django.db import models


# Create your models here.

# 图片表
class Image(models.Model):
    image = models.ImageField(upload_to='images', verbose_name='垃圾图片')
    name = models.CharField(max_length=20, verbose_name="名称")
    garbage_category = models.ForeignKey(to='GarbageCategory', verbose_name="垃圾类型类",
                                         on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = "图片类"


# 垃圾类别
class GarbageCategory(models.Model):
    name = models.CharField(max_length=24, verbose_name="名称")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = "垃圾类型分类表"
