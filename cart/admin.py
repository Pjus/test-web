from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'registered_date', 'cart_id']

class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'cart', 'active']
    list_per_page = 20


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)