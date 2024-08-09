from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import pytz

from .models import Quotation, Invoice, Item
from .forms import QuotationForm, InvoiceForm
from .decorators import super_admin_only
from helpers import utils
from django.forms import modelformset_factory

# Quotation Views
@method_decorator(super_admin_only, name='dispatch')
class QuotationListView(View):
    template_name = 'admin/quotation/quotation_list.html'

    def get(self, request):
        quotations = Quotation.objects.all()
        context = {'quotations': quotations}
        return render(request, self.template_name, context)


class QuotationDetailView(View):
    template_name = 'admin/quotation/quotation_detail.html'

    def get(self, request, pk):
        quotation = get_object_or_404(Quotation, pk=pk)
        context = {
            'quotation': quotation
        }
        return render(request, self.template_name, context)

ItemFormSet = modelformset_factory(Item, fields=('sr_no', 'name', 'description', 'quantity', 'amount'), extra=1, can_delete=True)

@method_decorator(super_admin_only, name='dispatch')
class QuotationCreateView(CreateView):
    model = Quotation
    form_class = QuotationForm
    template_name = 'admin/quotation/quotation_form.html'
    success_url = reverse_lazy('quotation:quotation_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['item_formset'] = ItemFormSet(self.request.POST)
        else:
            context['item_formset'] = ItemFormSet(queryset=Item.objects.none())
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        item_formset = context['item_formset']

        if form.is_valid() and item_formset.is_valid():
            form.instance.created_at = timezone.now()
            self.object = form.save()

            # Save items with automatic sr_no assignment
            items = item_formset.save(commit=False)
            last_sr_no = Item.objects.aggregate(max_sr_no=models.Max('sr_no'))['max_sr_no'] or 0

            for index, item in enumerate(items, start=1):
                item.quotation = self.object
                item.sr_no = last_sr_no + index
                item.save()

            return super().form_valid(form)
        else:
            return self.form_invalid(form)


@method_decorator(super_admin_only, name='dispatch')
class QuotationUpdateView(UpdateView):
    model = Quotation
    form_class = QuotationForm
    template_name = 'admin/quotation/quotation_form.html'
    success_url = reverse_lazy('quotation:quotation_list')


@method_decorator(super_admin_only, name='dispatch')
class QuotationDeleteView(DeleteView):
    model = Quotation
    template_name = 'admin/quotation/quotation_confirm_delete.html'
    success_url = reverse_lazy('quotation:quotation_list')


# Invoice Views
@method_decorator(super_admin_only, name='dispatch')
class InvoiceListView(View):
    template_name = 'admin/quotation/invoice_list.html'

    def get(self, request):
        invoices = Invoice.objects.all()
        context = {
            'invoices': invoices
        }
        return render(request, self.template_name, context)


@method_decorator(super_admin_only, name='dispatch')
class InvoiceDetailView(View):
    template_name = 'admin/quotation/invoice_detail.html'

    def get(self, request, pk):
        invoice = get_object_or_404(Invoice, pk=pk)
        context = {
            'invoice': invoice
        }
        return render(request, self.template_name, context)


@method_decorator(super_admin_only, name='dispatch')
class InvoiceCreateView(CreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'admin/quotation/invoice_form.html'
    success_url = reverse_lazy('quotation:invoice_list')


@method_decorator(super_admin_only, name='dispatch')
class InvoiceUpdateView(UpdateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'admin/quotation/invoice_form.html'
    success_url = reverse_lazy('quotation:invoice_list')


@method_decorator(super_admin_only, name='dispatch')
class InvoiceDeleteView(DeleteView):
    model = Invoice
    template_name = 'admin/quotation/invoice_confirm_delete.html'
    success_url = reverse_lazy('quotation:invoice_list')
