import os
from django.db import models
from django.conf import settings
from django.db.models.deletion import SET_NULL
from django.utils import timezone
from uuid import uuid4
from datetime import datetime


from users.choice import *
"""
교육
날짜
카테고리
제목
내용
동영상
"""

def get_file_path(instance, filename):
    ymd_path = datetime.now().strftime('%Y/%m/%d')
    uuid_name = uuid4().hex
    return ''.join(['upload_file/edu/', ymd_path, uuid_name])

class Product(models.Model):
    name = models.CharField(max_length=250, unique=True, verbose_name='상품명')
    description = models.TextField(blank=True, verbose_name='설명')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=128)
    price = models.IntegerField()
    upload_files = models.FileField(upload_to='product/', null=True, blank=True, verbose_name='파일')
    image = models.ImageField(upload_to="product/", null=True, blank=True, verbose_name='이미지')
    filename = models.CharField(max_length=64, null=True, verbose_name='첨부파일명')
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
    updated_date = models.DateTimeField(auto_now=True, verbose_name="업데이트")


    class Meta:
        ordering = ('name', )
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self) -> str:
        return f'{self.name}'


    def delete(self, *args, **kargs):
        if self.upload_files:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.upload_files.path))
        super(Product, self).delete(*args, **kargs)

    


class Videos(models.Model):
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to='videos/')
        
    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name = 'video'
        verbose_name_plural = 'videos'
