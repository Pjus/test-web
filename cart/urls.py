from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'cart'

urlpatterns = [
    path('add/', views.add_cart, name='add_cart'),
    path('', views.cart_detail, name="cart_detail"),
    path('remove/<int:product_id>/', views.delete_cartItem, name="cart_remove"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
