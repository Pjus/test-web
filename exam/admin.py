from django.contrib import admin

# Register your models here.
# Register your models here.
from .models import QuesModel, QuestionContents

class QuestionContentsAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'user',
        'catagory',
        'registered_date',
        )
    search_fields = ('title', 'user', 'catagory', 'registered_date')

# Register your models here.
admin.site.register(QuesModel)
admin.site.register(QuestionContents)