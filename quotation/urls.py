from django.urls import path
from . import views

app_name = 'quotation'

urlpatterns = [
    path('quotations/', views.QuotationListView.as_view(), name='quotation_list'),
    path('quotations/create/', views.QuotationCreateView.as_view(), name='quotation_create'),
    path('quotations/<int:pk>/delete/', views.QuotationDeleteView.as_view(), name='quotation_delete'),
    path('quotation/<int:pk>/', views.QuotationDetailView.as_view(), name='quotation_detail'),
    path('quotation/<int:id>/details/', views.QuotationDetailsView.as_view(), name='quotation_details'),
    path('create-invoice/', views.CreateInvoiceView.as_view(), name='create_invoice'),
    path('invoice/<int:invoice_id>/',views.InvoiceView.as_view(), name='invoice'),
]
