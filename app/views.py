from django.shortcuts import render
from django.http import HttpResponse
import pdfkit
from django.http import HttpResponse
from django.template.loader import render_to_string
import os

# Create your views here.

def home(request):
    # return HttpResponse('home')
    return render(request, 'home.html')


def render_pdf_view(request):
    # Render the HTML template
    html = render_to_string('home.html', {})

    # Define the path to the wkhtmltopdf executable
    # If wkhtmltopdf is installed globally, this may not be needed
    # path_to_wkhtmltopdf = r'C:\\Users\\ADMIN\\Downloads\\wkhtmltox-0.12.6-1.mxe-cross-win64\\wkhtmltox\\bin'  # Adjust the path based on your system
    # path_to_wkhtmltopdf = 'E:\Zzz\Zzzz\printer'
    # config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
    # print(config)
    # Convert HTML to PDF
    pdf = pdfkit.from_string(html, False) #, configuration=config)

    # Create HTTP response with the PDF
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="output.pdf"'

    return response
