from django.db import models
from edu.models import Product
from django.conf import settings
from django.db.models.deletion import SET_NULL
import random

from cert.models import Certification

def random_string():
    return str(random.randint(10000, 99999))

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=SET_NULL, null=True, verbose_name='구매자')
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
    cart_id = models.CharField(max_length=18, default = random_string)

    class Meta:
        db_table = "Cart"
        ordering = ['registered_date']

    def __str__(self):
        return f'{self.user}'

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = 1 # models.IntegerField()
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to="product/", null=True, blank=True, verbose_name='이미지')

    class Meta:
        db_table = "CartItem"
    
    def sub_total(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f'{self.product}'
    
    
class CertItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=SET_NULL, null=True, verbose_name='구매자')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = 1 # models.IntegerField()
    active = models.BooleanField(default=True, verbose_name="배송중")
    cert = models.ForeignKey(Certification, on_delete=models.CASCADE)
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')

    class Meta:
        db_table = "CertItem"
    
    def __str__(self):
        return f'{self.product}'
    