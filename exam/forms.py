from django import forms
from .models import QuizContents, Quiz

class addExamForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(addExamForm, self).__init__(*args, **kwargs)
        self.fields['quiz_title'].label = '제목'
        self.fields['quiz_title'].widget.attrs.update({
            'placeholder': '제목을 입력해주세요.',
            'class': 'form-control',
            'id': 'form_title',
            'autofocus': True,
        })
        self.fields['category'].label = '분류'
        self.fields['category'].widget.attrs.update({
            'placeholder': '분류를 입력해주세요.',
            'autofocus': True,
        })

        self.fields['product'].label = '교육'
        self.fields['product'].widget.attrs.update({
            'placeholder': '교육을 입력해주세요.',
            'autofocus': True,
        })
    class Meta:
        model = QuizContents
        fields = ['quiz_title', 'category', 'product']

class addQuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields="__all__"