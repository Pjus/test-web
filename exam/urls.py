from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'exam'

urlpatterns = [
    path('test/', views.exam_test_view, name='exam_test'),


    path('', views.ExamListView.as_view(), name='exam_list'),
    path('<int:pk>/', views.exam_detail_view, name='exam_detail'),

    path('write/', views.exam_write_view, name='exam_write'),
    path('quiz/', views.quiz_write_view, name='quiz_write'),
    path('<int:pk>/edit/', views.question_write_view, name='question_write'),
    path('<int:pk>/submit/', views.exam_submit_view, name='exam_submit'),




]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
