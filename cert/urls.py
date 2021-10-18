from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'cert'

urlpatterns = [
    path('', views.get_cert, name='certification'),
    path('<int:pk>/', views.GeneratePDF.as_view(), name='certdownload'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
