from django.contrib import admin
from .models import Certification

class CertAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'category', 'registered_date']
    list_per_page = 20


admin.site.register(Certification, CertAdmin)

