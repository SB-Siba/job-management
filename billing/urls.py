from django.urls import path
from .views import (
    QuotationListView, QuotationDetailView, QuotationCreateView,
    QuotationUpdateView, QuotationDeleteView,
    InvoiceListView, InvoiceDetailView, InvoiceCreateView,
    InvoiceUpdateView, InvoiceDeleteView
)

app_name = 'billing'

urlpatterns = [
    path('quotations/', QuotationListView.as_view(), name='quotation_list'),
    path('quotations/<int:pk>/', QuotationDetailView.as_view(), name='quotation_detail'),
    path('quotations/add/', QuotationCreateView.as_view(), name='quotation_add'),
    path('quotations/create/', QuotationCreateView.as_view(), name='quotation_create'),
    path('quotations/<int:pk>/update/', QuotationUpdateView.as_view(), name='quotation_update'),
    path('quotations/<int:pk>/delete/', QuotationDeleteView.as_view(), name='quotation_delete'),
    
    path('invoices/', InvoiceListView.as_view(), name='invoice_list'),
    path('invoices/<int:pk>/', InvoiceDetailView.as_view(), name='invoice_detail'),
    path('invoices/create/', InvoiceCreateView.as_view(), name='invoice_create'),
    path('invoices/add/', InvoiceCreateView.as_view(), name='invoice_add'),
    path('invoices/<int:pk>/update/', InvoiceUpdateView.as_view(), name='invoice_update'),
    path('invoices/<int:pk>/delete/', InvoiceDeleteView.as_view(), name='invoice_delete'),
]
