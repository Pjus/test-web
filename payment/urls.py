from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('payment/', views.payment_view, name='payment'),
    path('kakaoPaySuccess/', views.approval, name='payment_success'),



]
