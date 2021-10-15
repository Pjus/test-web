import os
from django.db import models
from django.conf import settings
from django.db.models.deletion import SET_NULL
from datetime import datetime
from uuid import uuid4
from users.choice import *

def get_file_path1(instance, filename):
    ymd_path = datetime.now().strftime('%Y/%m/%d')
    uuid_name = uuid4().hex
    return ''.join(['upload_file/cert/', ymd_path, uuid_name])

# Create your models here.
class Certification(models.Model):
    title = models.CharField(max_length=128, verbose_name='제목', default="")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=SET_NULL, null=True, verbose_name='사용자')
    catagory = models.CharField(choices=CATAGORY_CHOICES, max_length=128, verbose_name="분류")
    upload_files = models.FileField(upload_to=get_file_path1, null=True, blank=True, verbose_name='파일')
    filename = models.CharField(max_length=64, null=True, verbose_name='첨부파일명')
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')

