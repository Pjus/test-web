from django.urls import path
from . import views

app_name = 'cert'

urlpatterns = [
    path('', views.get_cert, name='certification'),
    path('<int:pk>/', views.GeneratePDF.as_view(), name='certdownload'),
]
