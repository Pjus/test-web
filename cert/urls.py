from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'cert'

urlpatterns = [
    path('', views.CertListView.as_view(), name='certification'),
    path('<int:pk>/', views.GeneratePDF.as_view(), name='certdownload'),
    # path('<int:pk>/original/', views.get_original, name='certdownload'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
