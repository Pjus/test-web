from django.urls import path
from . import views

app_name = 'exam'

urlpatterns = [
    path('', views.ExamListView.as_view(), name='exam_list'),
    path('write/', views.exam_write_view, name='exam_write'),
    path('<int:pk>/', views.exam_detail_view, name='exam_detail'),
    path('<int:pk>/edit/', views.question_write_view, name='question_write'),
    path('<int:pk>/test/', views.exam_test_view, name='exam_test'),


]
