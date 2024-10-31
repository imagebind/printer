from django.shortcuts import render
from django.http import HttpResponse
import pdfkit
from django.http import HttpResponse
from django.template.loader import render_to_string, get_template
from io import BytesIO
from .models import Customer, Payment
from collections import defaultdict
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.db.models import Case, When, IntegerField, Value
from django.utils import timezone
from uuid import uuid4
import razorpay
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.shortcuts import render, redirect
from .forms import CustomerForm
from .constants import RAZORPAY_API_ID, RAZORPAY_SECRET_KEY
from django.contrib import messages
from datetime import datetime


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
    data = {}
    state_districts = defaultdict(list)
    l = Customer.objects.values('state__name', 'district__name')
    for ll in l:
        state_districts[ll['state__name']].append(ll['district__name'])
    state_districts = dict(state_districts)
    states = list(set(state_districts.keys()))
    data['states'] = sorted(states)
    print(state_districts)
    data['statedict'] = state_districts
    return render(request, 'home.html', {'data': data})


@xframe_options_sameorigin
def render_pdf_view(request):
    html = render_to_string('home.html', {})
    pdf = pdfkit.from_string(html, False)
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
    state = request.GET.get('state')
    district = request.GET.get('district')
    substatus = request.GET.get('substatus')
    export = request.GET.get('export')

    if state and state != 'all' and district and district != 'all':
        cus_list = list(Customer.objects.annotate(
                is_expired=Case(
                    When(plan_expiration_date=None, then=Value(-1)),
                    When(plan_expiration_date__lt=timezone.now(), then=Value(1)),  # Expired
                    default=Value(0),  # Active
                    output_field=IntegerField()
                )
            ).filter(state__name=state, district__name=district).values(*required_cols))
    elif state and state != 'all' and district and district == 'all':
        cus_list = list(Customer.objects.annotate(
                is_expired=Case(
                    When(plan_expiration_date=None, then=Value(-1)),
                    When(plan_expiration_date__lt=timezone.now(), then=Value(1)),  # Expired
                    default=Value(0),  # Active
                    output_field=IntegerField()
                )
            ).filter(state__name=state).values(*required_cols))
    else:
        cus_list = list(Customer.objects.annotate(
                        is_expired=Case(
                            When(plan_expiration_date=None, then=Value(-1)),
                            When(plan_expiration_date__lt=timezone.now(), then=Value(1)),  
                            default=Value(0),  # Active
                            output_field=IntegerField()
                        )
                    ).all().values(*required_cols))

    substatus_map = {
        'INCOMPLETE': -1,
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


    if export == 'true':
        pdf = render_to_pdf( 'customerdata.html', {'data': cus_dict})
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = 'download.pdf'
        content = "attachmet; filename=%s" %(filename)
        response['Content-Disposition'] = content
        return response
    return render(request, 'customerdata.html', {'data': cus_dict})



def create_customer(request):
    payment_id = request.GET.get('payment_id')
    order_id = request.GET.get('order_id')
    signature = request.GET.get('signature')
    payment_status = ''
    if payment_id and order_id and not len(Payment.objects.filter(payment_id=payment_id)):
        client = razorpay.Client(auth=(RAZORPAY_API_ID, RAZORPAY_SECRET_KEY))
        payment = client.payment.fetch(payment_id)
        if payment["status"] == "captured":
            customer = Customer.objects.get(email=payment['email'].upper())
            new_payment = Payment(customer=customer, payment_id=payment['id'], order_id=order_id, signature=signature, amount=payment['amount'], payment_method=payment['method'],status=payment['status'])
            new_payment.save()
            print("Payment successful")
            customer.subscription_date = datetime.now()
            customer.save()
            payment_status = 'success'
        else:
            customer = Customer.objects.get(email=payment['email'].upper())
            new_payment = Payment(customer=customer, payment_id=payment['id'], order_id=order_id, signature=signature, amount=payment['amount'], payment_method=payment['method'],status=payment['status'])
            new_payment.save()
            print("Payment not successful")
            payment_status = 'failed'

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            new_customer = form.save()
            client = razorpay.Client(auth=(RAZORPAY_API_ID, RAZORPAY_SECRET_KEY))

            order_data = {
                'amount':  new_customer.plan.amount, 
                'currency': 'INR', 
                'receipt': uuid4().hex
            }
            payment = client.order.create(data=order_data)

            pay_data  = {
                'key': RAZORPAY_API_ID,
                'amount': payment['amount'] * 100,
                'company_name': 'Printer',
                'description': 'Printer',
                'order_id': payment['id'],
                'customer_name': new_customer.name,
                'customer_email': new_customer.email,
                'customer_contact': new_customer.cell_number
            }
            request.session['pay_data'] = pay_data
            return redirect('pay')
    else:
        form = CustomerForm()
        data = {'form': form, 'payment_status': payment_status}
    return render(request, 'customer_form.html', {'data': data})

def pay(request):
    pay_data = request.session.get('pay_data', None)
    return render(request, 'pay.html', {'data': pay_data})

from django.http import JsonResponse
from .models import District

def get_districts(request, state_id):
    districts = District.objects.filter(state_id=state_id).values('id', 'name')
    return JsonResponse(list(districts), safe=False)

