from django import forms
from .models import Certification

class CertificationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CertificationForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = '제목'

    class Meta:
        model = Certification
        fields = ['title', 'catagory', 'upload_files', 'registered_date', 'user']