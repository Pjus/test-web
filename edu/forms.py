from django import forms
from .models import Product

class ProductWriteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductWriteForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = '상품명'
        self.fields['name'].widget.attrs.update({
            'placeholder': '상품명을 입력해주세요.',
            'class': 'form-control',
            'id': 'form_title',
            'autofocus': True,
        })

    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'description', 'upload_files', 'image']


