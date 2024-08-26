from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.forms import modelformset_factory
from django.db import models

from .models import Quotation, Invoice, Item
from .forms import QuotationForm, CreateInvoiceForm
from .decorators import super_admin_only
from django import forms


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
        context = {'quotation': quotation}
        return render(request, self.template_name, context)


ItemFormSet = modelformset_factory(
    Item,
    fields=('sr_no', 'name', 'description', 'quantity', 'amount'),
    extra=1,
    can_delete=True
)
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

            # Redirect to GenerateInvoiceView after successfully saving the quotation
            return redirect('quotation:invoice_create', id=self.object.id)
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

class CreateInvoiceView(View):
    template_name = 'admin/quotation/create_invoice.html'

    def get(self, request):
        form = CreateInvoiceForm()
        formset = ItemFormSet()
        context = {
            'form': form,
            'formset': formset,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = CreateInvoiceForm(request.POST)
        formset = ItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            invoice = form.save(commit=False)  
            invoice.save() 
            for item_form in formset:
                item = item_form.save(commit=False)
                item.invoice = invoice  
                item.save()
            
            # Redirect to the InvoiceView with the specific invoice_id
            return redirect('quotation:invoice', invoice_id=invoice.id)

        context = {
            'form': form,
            'formset': formset,
        }
        return render(request, self.template_name, context)

class InvoiceView(View):
    template_name = 'admin/quotation/invoice.html'

    def get(self, request, invoice_id):
        # Fetch the specific invoice using the invoice_id
        invoice = Invoice.objects.get(id=invoice_id)
        
        # Prepare the context with the invoice data
        context = {
            'invoice': invoice,
        }
        
        # Render the template with the context
        return render(request, self.template_name, context)
