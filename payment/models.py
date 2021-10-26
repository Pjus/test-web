from django.db import models
from edu.models import Product
from django.conf import settings
from django.db.models.deletion import SET_NULL
from users.choice import *

# Create your models here.
class PurchasedItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=SET_NULL, null=True, verbose_name='구매자')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='상품명')
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name='구매일')
    certificated = models.BooleanField(default=False, verbose_name="수료여부")
    stayedTime = models.CharField(max_length=200, default='0', null=True, verbose_name="머문시간")

    class Meta:
        ordering = ('registered_date', )
        verbose_name = 'PurchasedItem'
        verbose_name_plural = 'PurchasedItem'

    def __str__(self) -> str:
        return f'{self.user}'

