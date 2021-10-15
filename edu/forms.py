from django import forms
from .models import EduContents

class EduWriteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EduWriteForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = '제목'
        self.fields['title'].widget.attrs.update({
            'placeholder': '제목을 입력해주세요.',
            'class': 'form-control',
            'id': 'form_title',
            'autofocus': True,
        })

    class Meta:
        model = EduContents
        fields = ['title', 'catagory', 'content', 'upload_files']