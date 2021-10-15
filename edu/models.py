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

# Create your models here.
class EduContents(models.Model):
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=SET_NULL, null=True, verbose_name='작성자')
    title = models.CharField(max_length=128, verbose_name='제목')
    catagory = models.CharField(choices=CATAGORY_CHOICES, max_length=128, verbose_name="분류")
    content = models.TextField(verbose_name='내용')
    hits = models.PositiveIntegerField(verbose_name='조회수', default=0)
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
    top_fixed = models.BooleanField(verbose_name='상단고정', default=False)
    upload_files = models.FileField(upload_to=get_file_path, null=True, blank=True, verbose_name='파일')
    filename = models.CharField(max_length=64, null=True, verbose_name='첨부파일명')

    def __str__(self):
        return self.title

    def delete(self, *args, **kargs):
        if self.upload_files:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.upload_files.path))
        super(EduContents, self).delete(*args, **kargs)

    class Meta:
        db_table = '교육자료'
        verbose_name = '교육자료'
        verbose_name_plural = '교육자료'

class Videos(models.Model):
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to='videos/')
        
    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name = 'video'
        verbose_name_plural = 'videos'

