from django.urls import path
from . import views

app_name = 'quotation'

urlpatterns = [
    path('choose_quotation/', views.ChooseQuotationView.as_view(), name='choose_quotation'),
    path('view_quotation/', views.ViewQuotationView.as_view(), name='view_quotation'),
    path('quotation_list/', views.QuotationListView1.as_view(), name='quotation_list'),
    path('quotation_list_2/', views.QuotationListView2.as_view(), name='quotation_list_2'),
    path('quotations/create/', views.QuotationCreateView.as_view(), name='quotation_create'),
    path('quotations/<int:pk>/delete/', views.QuotationDeleteView.as_view(), name='quotation_delete'),
    path('quotation_delete_2/<int:pk>/delete/', views.QuotationDeleteView2.as_view(), name='quotation_delete_2'),
    path('quotation/<int:pk>/', views.QuotationDetailView1.as_view(), name='quotation_details_1'),
    path('quotation/<int:pk>/details/', views.QuotationDetailsView2.as_view(), name='quotation_details_2'),
    path('quotation_create_2/', views.QuotationCreateView2.as_view(), name='quotation_create_2'),
    path('invoice/add/', views.InvoiceDetailCreateView.as_view(), name='invoice_add'),
    path('invoices/', views.InvoiceListView.as_view(), name='invoice_list'),
    path('invoices/<int:invoice_id>/details/', views.InvoiceDetailView.as_view(), name='invoice_details'),
    path('invoices/<int:pk>/delete/', views.InvoiceDeleteView.as_view(), name='invoice_delete'),
]
