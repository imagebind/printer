from django.urls import path, include
from .views import home, render_pdf_view, get_customer_data

urlpatterns = [
    path('', home, name='home'),
    path('cusdata', get_customer_data, name='customerdata'),
    path('pdf/', render_pdf_view, name='render_pdf_view'),
]
