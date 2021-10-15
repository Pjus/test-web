from django.contrib import admin

# Register your models here.
# Register your models here.
from .models import Videos, EduContents

class EduContentsAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'writer',
        'catagory',
        'hits',
        'registered_date',
        'upload_files',
        )
    search_fields = ('title', 'content', 'writer__user_id', 'catagory')

admin.site.register(EduContents, EduContentsAdmin)
admin.site.register(Videos)
