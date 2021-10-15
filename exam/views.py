from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View, ListView
from django.template.loader import get_template
from django.db.models import Q

from datetime import datetime
import exam
from users.decorators import * 
from .forms import *

from django.shortcuts import render, get_object_or_404, redirect


class ExamListView(ListView):
    model = QuestionContents
    paginate_by = 10
    template_name = 'exam/exam_list.html'
    context_object_name = 'notice_list' 

    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        notice_list = QuestionContents.objects.order_by('id') 
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



# 시험등록
@login_message_required
@admin_required
def exam_write_view(request):
    if request.method == "POST":
        form = addExamForm(request.POST)
        user = request.session['user_id']
        user_id = User.objects.get(user_id = user)

        if form.is_valid():
            exam = form.save(commit = False)
            exam.writer = user_id
            exam.save()
            return redirect('exam:exam_list')
    else:
        form = addQuestionForm()
    return render(request, "exam/exam_write.html", {'form': form})


@login_message_required
def exam_detail_view(request, pk):
    exam = get_object_or_404(QuestionContents, pk=pk)

    context = {
        'exam': exam,
    }

    return render(request, 'exam/exam_detail.html', context)


@login_message_required
@admin_required
def question_write_view(request, pk):
    exam = QuestionContents.objects.get(id=pk)
    
    if request.method == "POST":
        if(exam.writer == request.user or request.user.level == '0'):
            form = addExamForm(request.POST, instance=exam)
            if form.is_valid():
                exam = form.save(commit = False)
                exam.save()
                messages.success(request, "수정되었습니다.")
                return redirect('/exam/'+str(pk))
    else:
        exam = QuestionContents.objects.get(id=pk)
        if exam.writer == request.user or request.user.level == '0':
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
def exam_test_view(request, pk):
    exam = QuestionContents.objects.get(id=pk)
    return render(request)