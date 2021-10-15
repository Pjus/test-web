from django import forms
from .models import QuestionContents, QuesModel

# class addQuestionForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(addQuestionForm, self).__init__(*args, **kwargs)
#         self.fields['title'].label = '제목'
#         self.fields['title'].widget.attrs.update({
#             'placeholder': '제목을 입력해주세요.',
#             'class': 'form-control',
#             'id': 'form_title',
#             'autofocus': True,
#         })

#     class Meta:
#         model = QuestionContents
#         fields = ['title', 'catagory']


class addQuestionForm(forms.ModelForm):
    class Meta:
        model=QuesModel
        fields="__all__"