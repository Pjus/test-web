from django.contrib import admin

# Register your models here.
# Register your models here.
from .models import QuesModel, QuestionContents

class QuestionContentsAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'writer',
        'category',
        'registered_date',
        'passed'
        )
    search_fields = ('title', 'user', 'category', 'registered_date')

class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'category',
        )
    search_fields = ('title', 'category')

# Register your models here.
admin.site.register(QuesModel, QuestionAdmin)
admin.site.register(QuestionContents, QuestionContentsAdmin)