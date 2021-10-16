from django.contrib import admin

# Register your models here.
# Register your models here.
from .models import Videos, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'registered_date', 'updated_date', 'upload_files']
    list_editable = ['category', 'price', 'upload_files']
    list_per_page = 20


admin.site.register(Product, ProductAdmin)
admin.site.register(Videos)


