from django.db import models
from edu.models import Product
from django.conf import settings
from django.db.models.deletion import SET_NULL

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=SET_NULL, null=True, verbose_name='구매자')
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
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
    

