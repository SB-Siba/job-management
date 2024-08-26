from django.urls import path
from . import views

app_name = 'quotation'

urlpatterns = [
    path('quotations/', views.QuotationListView.as_view(), name='quotation_list'),
    path('quotations/create/', views.QuotationCreateView.as_view(), name='quotation_create'),
    path('quotations/<int:pk>/update/', views.QuotationUpdateView.as_view(), name='quotation_update'),
    path('quotations/<int:pk>/delete/', views.QuotationDeleteView.as_view(), name='quotation_delete'),
    path('create-invoice/', views.CreateInvoiceView.as_view(), name='create_invoice'),
    path('invoice/',views.InvoiceView.as_view(), name='invoice'),
]
