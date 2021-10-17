from django.urls import path
from . import views

app_name = 'edu'

urlpatterns = [
    path('', views.EduListView.as_view(), name='edu_list'),
    path('study_list/', views.StudyListView.as_view(), name='study_list'),
    # path('pdf', views.pdf_view, name='pdf'),
    path('<int:pk>/', views.edu_detail_view, name='edu_detail'),
    path('write/', views.edu_write_view, name='edu_write'),
    path('<int:pk>/edit/', views.edu_edit_view, name='edu_edit'),
    path('<int:pk>/delete/', views.edu_delete_view, name='edu_delete'),
    path('download/<int:pk>', views.edu_download_view, name="edu_download"),

    
]
