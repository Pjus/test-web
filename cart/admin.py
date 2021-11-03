from django.contrib import admin
from .models import Cart, CartItem, CertItem

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'registered_date', 'cart_id']

class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'cart', 'active']
    list_per_page = 20


class CertItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'cart', 'active', 'cert']
    list_per_page = 20



admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(CertItem, CertItemAdmin)
