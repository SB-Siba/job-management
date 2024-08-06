from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Quotation, Invoice
from .forms import QuotationForm, InvoiceForm
from .decorators import super_admin_only
from django.utils.decorators import method_decorator

# Quotation Views

class QuotationListView(ListView):
    model = Quotation
    template_name = 'admin/billing/quotation_list.html'
    context_object_name = 'quotations'

    
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class QuotationDetailView(DetailView):
    model = Quotation
    template_name = 'admin/billing/quotation_detail.html'
    context_object_name = 'quotation'

    @method_decorator(super_admin_only)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class QuotationCreateView(CreateView):
    model = Quotation
    form_class = QuotationForm
    template_name = 'admin/billing/quotation_form.html'
    success_url = reverse_lazy('billing:quotation_list')

    @method_decorator(super_admin_only)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class QuotationUpdateView(UpdateView):
    model = Quotation
    form_class = QuotationForm
    template_name = 'admin/billing/quotation_form.html'
    success_url = reverse_lazy('billing:quotation_list')

    @method_decorator(super_admin_only)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class QuotationDeleteView(DeleteView):
    model = Quotation
    template_name = 'admin/billing/quotation_confirm_delete.html'
    success_url = reverse_lazy('billing:quotation_list')

    @method_decorator(super_admin_only)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# Invoice Views

class InvoiceListView(ListView):
    model = Invoice
    template_name = 'admin/billing/invoice_list.html'
    context_object_name = 'invoices'

    @method_decorator(super_admin_only)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = 'admin/billing/invoice_detail.html'
    context_object_name = 'invoice'

    @method_decorator(super_admin_only)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class InvoiceCreateView(CreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'admin/billing/invoice_form.html'
    success_url = reverse_lazy('billing:invoice_list')

    @method_decorator(super_admin_only)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class InvoiceUpdateView(UpdateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'admin/billing/invoice_form.html'
    success_url = reverse_lazy('billing:invoice_list')

    @method_decorator(super_admin_only)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class InvoiceDeleteView(DeleteView):
    model = Invoice
    template_name = 'admin/billing/invoice_confirm_delete.html'
    success_url = reverse_lazy('billing:invoice_list')

    @method_decorator(super_admin_only)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
