from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'edu'

urlpatterns = [
    path('', views.EduListView.as_view(), name='edu_list'),
    path('study_list/', views.StudyListView.as_view(), name='study_list'),
    # path('pdf', views.pdf_view, name='pdf'),
    path('write/', views.edu_write_view, name='edu_write'),
    path('<int:pk>/', views.edu_detail_view, name='edu_detail'),
    path('<int:pk>/edit/', views.edu_edit_view, name='edu_edit'),
    path('<int:pk>/delete/', views.edu_delete_view, name='edu_delete'),
    path('<int:pk>/savetime/', views.saveTime, name='edu_save'),
    path('download/<int:pk>', views.edu_download_view, name="edu_download"),

    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
