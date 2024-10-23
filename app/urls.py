from django.urls import path, include
from .views import home, render_pdf_view

urlpatterns = [
    path('', home, name='home'),
    path('pdf/', render_pdf_view, name='render_pdf_view'),
]

