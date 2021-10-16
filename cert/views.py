from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template

from datetime import datetime
from .utils import render_to_pdf #created in step 4
from users.decorators import * 


# Create your views here.

@login_message_required
def get_cert(request):
    context = {
        
    }
    return render(request, 'cert/certification.html', context)


class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template('cert/invoice.html')

        context = {
            "invoice_id": 123,
            "customer_name": request.user,
            "amount": 1399.99,
            "today": datetime.today().strftime('%Y/%m/%d'),
        }
        
        html = template.render(context)
        pdf = render_to_pdf('cert/invoice.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = f"{datetime.today().strftime('%Y/%m/%d')}_{request.user}.pdf"
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")