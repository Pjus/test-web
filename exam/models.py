import os
from django.db import models
from django.conf import settings
from django.db.models.deletion import SET_NULL
from uuid import uuid4
from datetime import datetime

from users.choice import *

def get_file_path(instance, filename):
    ymd_path = datetime.now().strftime('%Y/%m/%d')
    uuid_name = uuid4().hex
    return ''.join(['upload_file/exam/', ymd_path, uuid_name])

# Create your models here.
class QuestionContents(models.Model):
    title = models.CharField(max_length=128, verbose_name='제목', unique=True)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=SET_NULL, null=True, verbose_name='작성자')
    catagory = models.CharField(choices=CATAGORY_CHOICES, max_length=128, verbose_name="분류")
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
    passed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def delete(self, *args, **kargs):
        if self.upload_files:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.upload_files.path))
        super(QuestionContents, self).delete(*args, **kargs)

    class Meta:
        db_table = '시험과목'
        verbose_name = '시험과목'
        verbose_name_plural = '시험과목'
        ordering = ["title"]


class QuesModel(models.Model):
    title = models.CharField(max_length=128, verbose_name='제목', unique=True)
    catagory = models.CharField(choices=CATAGORY_CHOICES, max_length=128, verbose_name="분류", null=True)
    question = models.CharField(max_length=200,null=True)
    op1 = models.CharField(max_length=200,null=True)
    op2 = models.CharField(max_length=200,null=True)
    op3 = models.CharField(max_length=200,null=True)
    op4 = models.CharField(max_length=200,null=True)
    ans = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'Questions'
        verbose_name = 'Questions'
        verbose_name_plural = 'Questions'
        ordering = ["title"]
