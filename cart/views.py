from django.shortcuts import render, redirect, get_object_or_404
from edu.models import Product
from .models import CartItem, Cart, CertItem
from django.core.exceptions import ObjectDoesNotExist
from users.decorators import *

from cert.models import Certification
# Create your views here.

@login_message_required
def _cart_id(request):
    cart = request.user
    return cart

@login_message_required
def add_cart(request):
    if request.method == "POST":
        selected = request.POST.getlist('selected')
        for product_id in selected:
            product = Product.objects.get(id=product_id)
            image = product.image
            try:
                cart = Cart.objects.get(user=_cart_id(request))
            except Cart.DoesNotExist:
                cart = Cart.objects.create(
                    user = _cart_id(request),
                )
                cart.save()
            try:
                cart_item = CartItem.objects.get(product=product, cart=cart, image=image)
                cart_item.save()
            except CartItem.DoesNotExist:
                cart_item = CartItem.objects.create(
                    product = product,
                    cart = cart,
                    image = image
                )
                cart_item.save()

    return redirect('cart:cart_detail')

@login_message_required
def cart_detail(request, total=0, counter=0, cart_items=None):
    try:
        cart = Cart.objects.get(user=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        if not cart_items:
            cart.delete()
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    
    context = {
        'cart_items' : cart_items,
        'total' : total,
        'counter' : counter,
    }
    return render(request, 'cart/cart.html', context)


@login_message_required
def delete_cartItem(request, product_id):
    cart = Cart.objects.get(user=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart:cart_detail')


@login_message_required
def add_cert(request, cert_id):
    print(cert_id)
    try:
        cart = Cart.objects.get(user=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            user = _cart_id(request),
        )
        cart.save()
    pro = Product.objects.get(id=cert_id)
    cert = Certification.objects.get(product=pro, user=request.user)
    
    context = {
        'cert_items' : cert,
    }
    return render(request, 'cart/cert_cart.html', context)
