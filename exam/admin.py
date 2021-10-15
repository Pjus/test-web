from django.contrib import admin

# Register your models here.
# Register your models here.
from .models import QuesModel, QuestionContents

class QuestionContentsAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'writer',
        'catagory',
        'registered_date',
        'passed'
        )
    search_fields = ('title', 'user', 'catagory', 'registered_date')

class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'catagory',
        )
    search_fields = ('title', 'catagory')

# Register your models here.
admin.site.register(QuesModel, QuestionAdmin)
admin.site.register(QuestionContents, QuestionContentsAdmin)