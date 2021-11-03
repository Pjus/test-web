import os
from django.db import models
from django.conf import settings
from django.db.models.deletion import SET_NULL
from datetime import datetime
from uuid import uuid4

from django.db.models.expressions import F

from users.choice import *
from edu.models import Product

def get_file_path1(instance, filename):
    ymd_path = datetime.now().strftime('%Y/%m/%d')
    uuid_name = uuid4().hex
    return ''.join(['upload_file/cert/', ymd_path, uuid_name])

# Create your models here.
class Certification(models.Model):
    name = models.CharField(max_length=250, unique=True, verbose_name='수료증명', default="")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=SET_NULL, null=True, verbose_name='사용자')
    user_name = models.CharField(max_length=128, verbose_name="사용자 이름",  default="",null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=128, verbose_name="분류", null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='상품명', default="")
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
    address = models.CharField(max_length=128, verbose_name="주소",  default="")
    price = models.IntegerField(default=30000, verbose_name="수료증 가격")


    def __str__(self) -> str:
        return f'{self.name}'

