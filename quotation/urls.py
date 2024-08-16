# quotation/urls.py

from django.urls import path
from . import views

app_name = 'quotation'

urlpatterns = [
    path('quotations/', views.QuotationListView.as_view(), name='quotation_list'),
    path('quotations/create/', views.QuotationCreateView.as_view(), name='quotation_create'),
    path('quotations/<int:pk>/update/', views.QuotationUpdateView.as_view(), name='quotation_update'),
    path('quotations/<int:pk>/delete/', views.QuotationDeleteView.as_view(), name='quotation_delete'),
    path('invoices/', views.InvoiceListView.as_view(), name='invoice_list'),
    path('invoices/add/', views.InvoiceCreateView.as_view(), name='create_invoice'),
    path('invoices/<int:pk>/', views.InvoiceDetailView.as_view(), name='invoice_detail'),
    path('invoices/<int:pk>/edit/', views.InvoiceUpdateView.as_view(), name='invoice_edit'),
    path('invoices/<int:pk>/delete/', views.InvoiceDeleteView.as_view(), name='invoice_delete'),
    
]