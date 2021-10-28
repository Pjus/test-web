from django.db import models
from django.db.models.fields import CharField
from users.choice import *
from django.conf import settings
from django.db.models.deletion import SET_NULL
from edu.models import Product

# Create your models here.

class QuizContents(models.Model):
    quiz_title = models.CharField(max_length=128, null=False, verbose_name="quiz_title")
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=128, verbose_name="분류")
    cert = models.BooleanField(default=False, verbose_name="수료여부")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='상품명', default='')
    num_exam = models.IntegerField(default=3, verbose_name="응시기회") 

    def __str__(self):
        return self.quiz_title

    class Meta:
        db_table = 'QuizContents'
        verbose_name = 'QuizContents'
        verbose_name_plural = 'QuizContents'
        ordering = ["quiz_title"]

class Quiz(models.Model):
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=128, verbose_name="분류", null=True)
    quiz_title = models.ForeignKey(QuizContents, on_delete=models.CASCADE, verbose_name="quiz_title")
    question = models.CharField(max_length=200,null=True)
    op1 = models.CharField(max_length=200,null=True)
    op2 = models.CharField(max_length=200,null=True)
    op3 = models.CharField(max_length=200,null=True)
    op4 = models.CharField(max_length=200,null=True)
    op5 = models.CharField(max_length=200,null=True)
    ans = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return f'{self.quiz_title}'
    
    class Meta:
        db_table = 'Quiz'
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quiz'
        ordering = ["quiz_title"]