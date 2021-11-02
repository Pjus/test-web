from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib import messages

from edu.models import Product

from .models import PurchasedItem

from cart.models import Cart, CartItem
from cart.views import _cart_id
import requests

from users.decorators import *
from .models import PurchasedItem
from cert.models import Certification

from django.db.models import Q

# Create your views here.
@login_message_required
def payment_view(request):
    current_full_url = request.build_absolute_uri()
    url_path = request.path
    target_url = current_full_url.replace(url_path, '')
    print(target_url)
    current_user = str(request.user)
    cart = Cart.objects.get(user=_cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart, active=True)
    content = {
        'cart' : cart_items,
    }

    if request.method == "POST":
        URL = 'https://kapi.kakao.com/v1/payment/ready'
        headers = {
            "Authorization": "KakaoAK " + "c7d8f589a61b699314201b6e1cc9f8c6",   # 변경불가
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",  # 변경불가
        }
        if len(cart_items) > 1:
            items = f'{cart_items[0].product.name}외 {len(cart_items)-1}건'
        else:
            items = cart_items[0].product.name

        quantity = [item.quantity for item in cart_items]
        total_amount = [item.product.price for item in cart_items]
        params = {
            "cid": "TC0ONETIME",    # 테스트용 코드
            "partner_order_id": cart.cart_id,     # 주문번호
            "partner_user_id": current_user,    # 유저 아이디
            "item_name": items,        # 구매 물품 이름
            "quantity": sum(quantity),                # 구매 물품 수량
            "total_amount": sum(total_amount),        # 구매 물품 가격
            "tax_free_amount": "0",         # 구매 물품 비과세
            "approval_url": f"{target_url}/payment/kakaoPaySuccess/",
            "cancel_url": f"{target_url}/cart/",
            "fail_url": f"{target_url}/cart/",
        }
        

        res = requests.post(URL, headers=headers, params=params)
        request.session['tid'] = res.json()['tid']      # 결제 승인시 사용할 tid를 세션에 저장
        next_url = res.json()['next_redirect_pc_url']   # 결제 페이지로 넘어갈 url을 저장
        print(request.session['tid'])
        return redirect(next_url)

    return render(request, 'payment/payment.html', content)

@login_message_required
def approval(request):
    current_user = str(request.user)
    cart = Cart.objects.get(user=_cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart, active=True)
    for item in cart_items:
        product = Product.objects.get(name=item.product.name)
        print(product)
        try:
            purchased = PurchasedItem.objects.get(user=request.user, product = product)
            purchased.save()
        except PurchasedItem.DoesNotExist:
            purchased = PurchasedItem.objects.create(
                user = request.user,
                product = product,
            )
            purchased.save()

    cart = Cart.objects.get(user=_cart_id(request))
    URL = 'https://kapi.kakao.com/v1/payment/approve'

    headers = {
        "Authorization": "KakaoAK " + "c7d8f589a61b699314201b6e1cc9f8c6",
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    }
    
    params = {
        "cid": "TC0ONETIME",    # 테스트용 코드
        "tid": request.session['tid'],  # 결제 요청시 세션에 저장한 tid
        "partner_order_id": cart.cart_id,     # 주문번호
        "partner_user_id": current_user,    # 유저 아이디
        "pg_token": request.GET.get("pg_token"),     # 쿼리 스트링으로 받은 pg토큰
    }

    res = requests.post(URL, headers=headers, params=params)
    amount = res.json()['amount']['total']
    res = res.json()
    context = {
        'res': res,
        'amount': amount,
    }
    cart.delete()
    return render(request, 'payment/approval.html', context)


class PaidListView(ListView):
    model = PurchasedItem
    paginate_by = 10
    template_name = 'payment/paid_list.html'  #DEFAULT : <app_label>/<model_name>_list.html
    context_object_name = 'notice_list'        #DEFAULT : <model_name>_list html name
    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        notice_list = PurchasedItem.objects.order_by('id') 
        if search_keyword :
            if len(search_keyword) > 1 :
                if search_type == 'all':
                    search_notice_list = notice_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword) | Q (writer__user_id__icontains=search_keyword))
                elif search_type == 'title':
                    search_notice_list = notice_list.filter(title__icontains=search_keyword)    
                elif search_type == 'catagory':
                    search_notice_list = notice_list.filter(catagory__icontains=search_keyword)    
                return search_notice_list
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
        return notice_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range

        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')

        if len(search_keyword) > 1 :
            context['q'] = search_keyword
        context['type'] = search_type

        return context



@login_message_required
def payment_cert_view(request):
    current_full_url = request.build_absolute_uri()
    url_path = request.path
    target_url = current_full_url.replace(url_path, '')
    print(target_url)
    current_user = str(request.user)
    cart = Cart.objects.get(user=_cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart, active=True)
    content = {
        'cart' : cart_items,
    }

    if request.method == "POST":
        URL = 'https://kapi.kakao.com/v1/payment/ready'
        headers = {
            "Authorization": "KakaoAK " + "c7d8f589a61b699314201b6e1cc9f8c6",   # 변경불가
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",  # 변경불가
        }
        if len(cart_items) > 1:
            items = f'{cart_items[0].product.name}외 {len(cart_items)-1}건'
        else:
            items = cart_items[0].product.name

        quantity = [item.quantity for item in cart_items]
        total_amount = [item.product.price for item in cart_items]
        params = {
            "cid": "TC0ONETIME",    # 테스트용 코드
            "partner_order_id": cart.cart_id,     # 주문번호
            "partner_user_id": current_user,    # 유저 아이디
            "item_name": items,        # 구매 물품 이름
            "quantity": sum(quantity),                # 구매 물품 수량
            "total_amount": sum(total_amount),        # 구매 물품 가격
            "tax_free_amount": "0",         # 구매 물품 비과세
            "approval_url": f"{target_url}/payment/kakaoPaySuccess/",
            "cancel_url": f"{target_url}/cart/",
            "fail_url": f"{target_url}/cart/",
        }
        

        res = requests.post(URL, headers=headers, params=params)
        request.session['tid'] = res.json()['tid']      # 결제 승인시 사용할 tid를 세션에 저장
        next_url = res.json()['next_redirect_pc_url']   # 결제 페이지로 넘어갈 url을 저장
        print(request.session['tid'])
        return redirect(next_url)

    return render(request, 'payment/payment.html', content)