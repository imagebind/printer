from django.shortcuts import render
from django.http import HttpResponse
import pdfkit
from django.http import HttpResponse
from django.template.loader import render_to_string, get_template
from io import BytesIO
import os
from .models import Customer
# Create your views here.
from collections import defaultdict
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.db.models import Case, When, IntegerField, Value
from django.utils import timezone

from django.template.loader import render_to_string
# from weasyprint import HTML
from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

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
        'door_number',
        'street_name',
        'area',
        'taluk',
        'district',
        'state',
        'pincode',
        'landmark',
        'subscription_date',
        'plan_expiration_date',
        'is_expired',
    ]
    # print(request.GET)
    state = request.GET.get('state')
    district = request.GET.get('district')
    substatus = request.GET.get('substatus')
    export = request.GET.get('export')
    print(state, district, substatus)
    if state and state != 'all' and district and district != 'all':
        cus_list = list(Customer.objects.annotate(
                is_expired=Case(
                    When(plan_expiration_date__lt=timezone.now(), then=Value(1)),  # Expired
                    default=Value(0),  # Active
                    output_field=IntegerField()
                )
            ).filter(state=state, district=district).values(*required_cols))
    elif state and state != 'all' and district and district == 'all':
        cus_list = list(Customer.objects.annotate(
                is_expired=Case(
                    When(plan_expiration_date__lt=timezone.now(), then=Value(1)),  # Expired
                    default=Value(0),  # Active
                    output_field=IntegerField()
                )
            ).filter(state=state).values(*required_cols))
    else:
        cus_list = list(Customer.objects.annotate(
                        is_expired=Case(
                            When(plan_expiration_date__lt=timezone.now(), then=Value(1)),  # Expired
                            default=Value(0),  # Active
                            output_field=IntegerField()
                        )
                    ).all().values(*required_cols))

    substatus_map = {
        'LIVE': 0,
        'EXPIRED': 1
    }

    if substatus and substatus != 'all':
        cus_list = [customer for customer in cus_list if customer['is_expired']==substatus_map[substatus.upper()]]

    cus_dict = {}
    
    for customer in cus_list:
        if customer['district'] not in cus_dict.keys():
            cus_dict[customer['district']] = []
        cus_dict[customer['district']].append(customer)

    
    cus_dict = sorted(cus_dict.items())
    print(len(cus_dict), cus_dict)

    if export == 'true':
        pdf = render_to_pdf( 'customerdata.html', {'data': cus_dict})
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = 'download.pdf'
        content = "attachmet; filename=%s" %(filename)
        response['Content-Disposition'] = content
        return response

        #############################
        # html = render_to_string( 'customerdata.html', {'data': cus_list})
        # options = {
        #     'page-size': 'A4',
        #     'disable-javascript': '',
        #     'load-error-handling': 'ignore',
        #     # 'load-timeout': '10.0',
        #     'enable-local-file-access': ''
        # }
        # pdf = pdfkit.from_string(html, 'output.pdf', options=options)
        # response = HttpResponse(pdf, content_type='application/pdf')
        # response['Content-Disposition'] = 'attachment; filename="output.pdf"'
        # return response
        ####################################
        # html_string = render_to_string( 'customerdata.html', {'data': cus_list})
        # pdf = html(string=html_string).write_pdf()
        # response = HttpResponse(pdf, content_type='application/pdf')
        # response['Content-Disposition'] = 'inline; filename="report.pdf"'
        # return response
    return render(request, 'customerdata.html', {'data': cus_dict})

from django.shortcuts import render, redirect
from .forms import CustomerForm

def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Redirect to a success page or customer list
    else:
        form = CustomerForm()
    return render(request, 'customer_form.html', {'form': form})

