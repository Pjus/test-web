from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'payment'

urlpatterns = [
    path('payment/', views.payment_view, name='payment'),
    path('payment/cert/', views.payment_cert_view, name='cert_payment'),
    path('kakaoPaySuccess/', views.approval, name='payment_success'),




] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
