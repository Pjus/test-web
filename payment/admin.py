from django.contrib import admin
from .models import PurchasedItem


class PurchasedAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'registered_date', 'certificated']

admin.site.register(PurchasedItem, PurchasedAdmin)


