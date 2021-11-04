from django.db.models.query import prefetch_related_objects
from django.forms.widgets import PasswordInput
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import View, ListView
from django.template.loader import get_template, render_to_string
from django.db.models import Q

from datetime import datetime, timedelta
import exam
from users.decorators import * 
from .forms import *
from .models import Quiz, QuizContents
from payment.models import PurchasedItem
from django.shortcuts import render, get_object_or_404, redirect

import json

class ExamListView(ListView):
    model = QuizContents
    bought_items = PurchasedItem
    paginate_by = 10
    template_name = 'exam/exam_list.html'
    context_object_name = 'exam_list' 

    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')

        study_list = PurchasedItem.objects.filter(user=self.request.user)
        exam_list = []
        try:
            for item in study_list:
                print(item.product)
                studied_time = item.total_time
                try:
                    (h, m, s) = studied_time.split(':')
                    time = timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                except:
                    time = timedelta(hours=int(0), minutes=int(0), seconds=int(0))

                if time > timedelta(hours=int(0), minutes=int(20), seconds=int(0)):
                    exam_item = QuizContents.objects.get(product=item.product)
                    exam_item.study_cert = True
                    if item.certificated == True:
                        exam_item.cert = True
                else:
                    exam_item = QuizContents.objects.get(product=item.product)
                    exam_item.study_cert = False

                exam_list.append(exam_item)
        except:
            pass

        if search_keyword :
            if len(search_keyword) > 1 :
                if search_type == 'all':
                    search_notice_list = exam_list.filter(Q (quiz_title__icontains=search_keyword) | Q (category__icontains=search_keyword))
                elif search_type == 'title':
                    search_notice_list = exam_list.filter(quiz_title_icontains=search_keyword)    
                elif search_type == 'catagory':
                    search_notice_list = exam_list.filter(category__icontains=search_keyword)    
                return search_notice_list
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
        return exam_list

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



# 시험등록
@login_message_required
@admin_required
def exam_write_view(request):
    if request.method == "POST":
        QuizContentForm = addExamForm(request.POST)
        if QuizContentForm.is_valid():
            exam = QuizContentForm.save(commit = False)
            exam.save()
            return redirect('exam:exam_list')
    else:
        QuizContentForm = addExamForm()
    return render(request, "exam/exam_write.html", {'QuizContentForm': QuizContentForm})

# 퀴즈등록
@login_message_required
@admin_required
def quiz_write_view(request):
    if request.method == "POST":
        QuizForm = addQuizForm(request.POST)
        print(QuizForm.is_valid())
        if QuizForm.is_valid():
            quiz = QuizForm.save(commit = False)
            quiz.save()
            return redirect('exam:exam_list')
    else:
        QuizForm = addQuizForm()
    return render(request, "exam/quiz_write.html", {'QuizForm':QuizForm})


@login_message_required
@admin_required
def question_write_view(request, pk):
    exam = QuizContents.objects.get(id=pk)
    
    if request.method == "POST":
        if(exam.writer == request.user or request.user.level == '0'):
            form = addExamForm(request.POST, instance=exam)
            if form.is_valid():
                exam = form.save(commit = False)
                exam.save()
                messages.success(request, "수정되었습니다.")
                return redirect('/exam/'+str(pk))
    else:
        exam = QuizContents.objects.get(id=pk)
        if request.user.level == '0':
            form = addExamForm(instance=exam)
            context = {
                'form': form,
                'edit': '수정하기',
            }
            return render(request, "exam/exam_write.html", context)
        else:
            messages.error(request, "본인 게시글이 아닙니다.")
            return redirect('/exam/'+str(pk))

@login_message_required
def exam_test_view(request):
    return render(request, 'exam/test.html')

@login_message_required
def exam_submit_view(request, name):
    exam = get_object_or_404(QuizContents, name=name)
    title = exam
    quizs = Quiz.objects.filter(quiz_title=title)

    context = {
        'exam': exam,
        'quiz_list':quizs,
        'passed':'',
    }
    return render(request, 'exam/exam_detail.html', context)



@login_message_required
def exam_detail_view(request, pk):
    print(request.session)
    exam = get_object_or_404(QuizContents, product_id=pk)
    exam.num_exam -= 1
    exam.save()
    title = exam
    quizs = Quiz.objects.filter(quiz_title=title)

    context = {
        'exam': exam,
        'quiz_list':quizs,
    }
    return render(request, 'exam/exam_detail.html', context)


@login_message_required
def exam_submit_view(request, pk):
    users_ans = json.loads(request.body,  encoding="UTF-8")
    score = 0
    real_ans = {}
    exam = QuizContents.objects.get(product_id=pk)
    title = exam
    quizs = Quiz.objects.filter(quiz_title=title)
    certificated = False

    for quiz in quizs:
        real_ans[str(quiz.id)] = quiz.ans
    print(real_ans)
    print(users_ans)

    for question, answer in real_ans.items():
        if users_ans[question] == answer:
            score += 20

    purchaseds = PurchasedItem.objects.filter(user=request.user)
    for item in purchaseds:
        if item.product.id == pk:
            if item.certificated == False:
                if score >= 60:
                    print('cert')
                    certificated = True
                    item.certificated = certificated
                    item.save()
                else:
                    print('Failed')
                    certificated = False
    context = {
        'score' : score,
        'certificated' : certificated,
    }
    return HttpResponse(json.dumps(context), content_type="application/json")

