import re
import urllib
import os
import mimetypes
import natsort
import json
import datetime

from django.conf import settings
from django.views.generic import ListView
from users.decorators import login_message_required, admin_required
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import redirect
from django.http import HttpResponse, Http404, request, response

# Search
from django.contrib import messages
from django.db.models import Q

from .forms import ProductWriteForm
from .models import Product, Videos
from users.models import User
from users.decorators import admin_required
from users.choice import CATEGORY_CHOICES

from payment.models import PurchasedItem

#show pdf
import fitz

class EduListView(ListView):
    model = Product
    paginate_by = 10
    template_name = 'edu/edu_list.html'  #DEFAULT : <app_label>/<model_name>_list.html
    context_object_name = 'notice_list'        #DEFAULT : <model_name>_list html name
    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        notice_list = Product.objects.order_by('id') 
        if search_keyword :
            if len(search_keyword) > 1 :
                if search_type == 'all':
                    search_notice_list = notice_list.filter(Q (name__icontains=search_keyword) | Q (category__icontains=search_keyword))
                elif search_type == 'title':
                    search_notice_list = notice_list.filter(name__icontains=search_keyword)    
                elif search_type == 'catagory':
                    search_notice_list = notice_list.filter(category__icontains=search_keyword)    
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



# 교육자료 게시글 보기
@login_message_required
def edu_detail_view(request, pk):
    notice = get_object_or_404(Product, pk=pk)
    path_dir = f"{settings.STATICFILES_DIRS[0]}/img/{notice.name}"
    imgs = []
    if notice.upload_files:
        filepath = settings.MEDIA_ROOT + "/" + str(notice.upload_files)
        doc = fitz.open(filepath)
        if os.path.isdir(path_dir):
            imgs = os.listdir(path_dir)
        else:
            os.mkdir(path_dir)
            for idx, pg in enumerate(doc):
                pix = pg.getPixmap()
                output = f"{path_dir}/outfile_{idx}.png"
                pix.writePNG(output)
        imgs = os.listdir(path_dir)
        imgs = [f"{notice.name}/{i}" for i in imgs]
        imgs = natsort.natsorted(imgs)
        
        context = {
            'notice': notice,
            'imgList': imgs,
            'page1':imgs[0],
        }
        return render(request, 'edu/edu_detail.html', context)

# 글쓰기
@login_message_required
@admin_required
def edu_write_view(request):
    if request.method == "POST":
        form = ProductWriteForm(request.POST)
        
        if form.is_valid():
            product = form.save(commit = False)
            if request.FILES:
                try:
                    if 'upload_files' in request.FILES.keys():
                        product.filename = request.FILES['upload_files'].name
                        product.upload_files = request.FILES['upload_files']
                        product.image = request.FILES['image']
                except:
                    print("err")
            product.save()
            return redirect('edu:edu_list')
    else:
        form = ProductWriteForm()

    return render(request, "edu/edu_write.html", {'form': form})

# 수정
@admin_required
def edu_edit_view(request, pk):
    notice = Product.objects.get(id=pk)
    
    if request.method == "POST":
        if(request.user.level == '0'):
            form = ProductWriteForm(request.POST, instance=notice)
            if form.is_valid():
                notice = form.save(commit = False)
                notice.save()
                messages.success(request, "수정되었습니다.")
                return redirect('/edu/'+str(pk))
    else:
        notice = Product.objects.get(id=pk)
        if request.user.level == '0':
            form = ProductWriteForm(instance=notice)
            context = {
                'form': form,
                'edit': '수정하기',
            }
            return render(request, "edu/edu_write.html", context)
        else:
            return redirect('/edu/'+str(pk))


# 삭제

@admin_required
def edu_delete_view(request, pk):
    notice = Product.objects.get(id=pk)
    if request.user.level == '0':
        notice.delete()
        messages.success(request, "삭제되었습니다.")
        return redirect('/edu/')
    else:
        return redirect('/edu/'+str(pk))


@login_message_required
def edu_download_view(request, pk):
    notice = get_object_or_404(Product, pk=pk)
    url = notice.upload_files.url[1:]
    file_url = urllib.parse.unquote(url)
    
    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            quote_file_url = urllib.parse.quote(notice.filename.encode('utf-8'))
            response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(file_url)[0])
            response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
            return response
        raise Http404



class StudyListView(ListView):
    model = PurchasedItem
    products = Product
    paginate_by = 10
    template_name = 'edu/study_list.html'  #DEFAULT : <app_label>/<model_name>_list.html
    context_object_name = 'study_list'        #DEFAULT : <model_name>_list html name
    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')

        study_list = PurchasedItem.objects.filter(user=self.request.user)

        if search_keyword :
            if len(search_keyword) > 1 :
                if search_type == 'all':
                    search_notice_list = study_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword) | Q (writer__user_id__icontains=search_keyword))
                elif search_type == 'title':
                    search_notice_list = study_list.filter(title__icontains=search_keyword)    
                elif search_type == 'catagory':
                    search_notice_list = study_list.filter(catagory__icontains=search_keyword)    
                return search_notice_list
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
        return study_list

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
def saveTime(request, pk):
    products = Product.objects.get(id=pk)
    if request.is_ajax():
        times = request.POST.get('times')
        times = json.loads(times)
        page_num = request.POST.get('current_page')
        item = PurchasedItem.objects.get(user=request.user, product=products)
   
        if item.stayedTime == {}: 
            item.stayedTime = times
            item.save()
        else:
            mysum = datetime.timedelta()
            exist_time = item.stayedTime[page_num]
            new_time = times[page_num]
            (h1, m1, s1) = exist_time.split(':')
            (h2, m2, s2) = new_time.split(':')

            d1 = datetime.timedelta(hours=int(h1), minutes=int(m1), seconds=int(s1))
            d2 = datetime.timedelta(hours=int(h2), minutes=int(m2), seconds=int(s2))

            total = d1 + d2
            mysum += total
            item.stayedTime[page_num] = str(mysum)
            item.save()

        total_time = datetime.timedelta()
        for page in item.stayedTime:
            (h2, m2, s2) = item.stayedTime[page].split(':')
            d2 = datetime.timedelta(hours=int(h2), minutes=int(m2), seconds=int(s2))
            total_time += d2
        item.total_time = total_time
        item.save()

        context = {
            'total_time' : str(item.total_time),
        }
        return HttpResponse(json.dumps(context), content_type="application/json")
