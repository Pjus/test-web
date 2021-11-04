from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View, ListView
from django.template.loader import get_template

from datetime import datetime
from .utils import render_to_pdf #created in step 4
from users.decorators import * 
from users.models import User

from edu.models import Product
from payment.models import PurchasedItem
# Create your views here.

from .models import Certification

from reportlab.pdfgen import canvas
from datetime import datetime
from cart.models import Cart, CertItem
import json
from django.core.serializers.json import DjangoJSONEncoder

from django.db.models import Q

from cert import models

class CertListView(ListView):
    model = PurchasedItem
    paginate_by = 10
    template_name = 'cert/certification.html'  #DEFAULT : <app_label>/<model_name>_list.html
    context_object_name = 'cert_list'        #DEFAULT : <model_name>_list html name
    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')

        cert_list = PurchasedItem.objects.filter(user=self.request.user, certificated=True)
        if search_keyword :
            if len(search_keyword) > 1 :
                if search_type == 'all':
                    search_notice_list = cert_list.filter(Q (quiz_title__icontains=search_keyword) | Q (category__icontains=search_keyword))
                elif search_type == 'title':
                    search_notice_list = cert_list.filter(quiz_title__icontains=search_keyword)    
                elif search_type == 'catagory':
                    search_notice_list = cert_list.filter(category__icontains=search_keyword)    
                return search_notice_list
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
        return cert_list


class GeneratePDF(View):
    def get(self, request, pk):
        template = get_template('cert/invoice.html')
        product_name = Product.objects.get(id=pk)
        current_user = User.objects.get(user_id=request.user)
        print(request.user)
        print(current_user.name)
        print(current_user.email)

        category_name = product_name.category
        category_name.encode('utf-8')
        context = {
            "product_name": product_name.name,
            "customer_name": current_user.name,
            "cert": True,
            "category": category_name,
            "today": datetime.today().strftime('%Y/%m/%d'),
        }
        try:
            cert = Certification.objects.get(user=request.user, product=product_name)
        except:
            cert = Certification.objects.create(
                user = request.user,
                user_name = current_user.name,
                category = category_name,
                product = product_name,
            )
            cert.save()

        pdf = render_to_pdf('cert/invoice.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = f"{datetime.today().strftime('%Y/%m/%d')}_{product_name.category}_{current_user.name}.pdf"
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            response.encoding = 'utf-8'
            return response
        return HttpResponse("Not found")



def cert_add_save(request):
    if request.is_ajax():
        print('ajax')
        cert_data = json.loads(request.body,  encoding="UTF-8")
        product_id = cert_data['product_id']
        product_name = Product.objects.get(id=product_id)
        cert_add = cert_data['cert_add']
        cert_buy = Certification.objects.get(user=request.user, product=product_name)
        cert_buy.address = cert_add
        cert_buy.save()


        context = {
            'cert' : cert_buy.address
        }
        return HttpResponse(json.dumps(context), content_type="application/json")


class CertCheckListView(ListView):
    model = CertItem
    paginate_by = 10
    template_name = 'cert/reqcheck.html'  #DEFAULT : <app_label>/<model_name>_list.html
    context_object_name = 'cert_list'        #DEFAULT : <model_name>_list html name
    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        cert_list = CertItem.objects.order_by('id')
        if search_keyword :
            if len(search_keyword) > 1 :
                if search_type == 'all':
                    search_notice_list = cert_list.filter(Q (quiz_title__icontains=search_keyword) | Q (category__icontains=search_keyword))
                elif search_type == 'title':
                    search_notice_list = cert_list.filter(quiz_title__icontains=search_keyword)    
                elif search_type == 'catagory':
                    search_notice_list = cert_list.filter(category__icontains=search_keyword)    
                return search_notice_list
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
        return cert_list
