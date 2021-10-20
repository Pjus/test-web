from django.contrib import admin

# Register your models here.
# Register your models here.
from .models import Quiz, QuizContents

class QuizContentsAdmin(admin.ModelAdmin):
    list_display = (
        'quiz_title', 
        'category',
        )
    search_fields = ('quiz_title', 'category')

class QuizAdmin(admin.ModelAdmin):
    list_display = (
        'quiz_title', 
        'category',
        )
    search_fields = ('quiz_title', 'category')

# Register your models here.
admin.site.register(Quiz, QuizAdmin)
admin.site.register(QuizContents, QuizContentsAdmin)