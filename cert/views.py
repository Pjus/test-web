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


from reportlab.pdfgen import canvas
from datetime import datetime

class CertListView(ListView):
    model = PurchasedItem
    paginate_by = 10
    template_name = 'cert/certification.html'  #DEFAULT : <app_label>/<model_name>_list.html
    context_object_name = 'cert_list'        #DEFAULT : <model_name>_list html name

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

def pdf_dw(request, pk):                                  
    
    # Create the HttpResponse object 
    response = HttpResponse(content_type='application/pdf') 

    # This line force a download
    response['Content-Disposition'] = 'attachment; filename="1.pdf"' 

    # READ Optional GET param
    get_param = request.GET.get('name', 'World')

    # Generate unique timestamp
    ts = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')

    p = canvas.Canvas(response)

    # Write content on the PDF 
    p.drawString(100, 500, "한글 " + get_param + " (Dynamic PDF) - " + ts ) 

    # Close the PDF object. 
    p.showPage() 
    p.save() 

    # Show the result to the user    
    return response