from django.urls import path
from . import views

app_name = 'exam'

urlpatterns = [
    path('', views.ExamListView.as_view(), name='exam_list'),
    path('write/', views.exam_write_view, name='exam_write'),

]
