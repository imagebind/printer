from django.urls import path, include
from .views import home, render_pdf_view, get_customer_data, create_customer, get_districts, pay, verify_customer
from .views import CustomLoginView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', home, name='home'),
    path('cusdata', get_customer_data, name='customerdata'),
    path('pdf/', render_pdf_view, name='render_pdf_view'),
    path('subscription-page/', create_customer, name='customerform'),
    path('get-districts/<int:state_id>/', get_districts, name='get_districts'),
    path('pay/', pay, name='pay'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify-customer/', verify_customer, name='verify_customer'),
]

