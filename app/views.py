from django.shortcuts import render
from django.http import HttpResponse
import pdfkit
from django.http import HttpResponse
from django.template.loader import render_to_string
import os
from .models import Customer
# Create your views here.
from collections import defaultdict
from django.views.decorators.clickjacking import xframe_options_sameorigin


@xframe_options_sameorigin
def home(request):
    # return HttpResponse('home')
    data = {}

    state_districts = defaultdict(list)
    l = Customer.objects.values('state', 'district')
    for ll in l:
        state_districts[ll['state']].append(ll['district'])
    state_districts = dict(state_districts)
    states = list(set(state_districts.keys()))
    data['states'] = sorted(states)
    print(state_districts)
    data['statedict'] = state_districts
    return render(request, 'home.html', {'data': data})


@xframe_options_sameorigin
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

@xframe_options_sameorigin
def get_customer_data(request):
    required_cols = [
        'name',
        'flat_no',
        'flat_name',
        'door_numbeer',
        'street_name',
        'area',
        'taluk',
        'district',
        'state',
        'pincode',
        'landmark',
    ]
    print(request.GET)
    state = request.GET.get('state')
    district = request.GET.get('district')
    substatus = request.GET.get('substatus')
    print(state, district, substatus)
    cus_list = list(Customer.objects.filter(state=state, district=district).values(*required_cols))
    print(cus_list)
    return render(request, 'customerdata.html', {'data': cus_list})

