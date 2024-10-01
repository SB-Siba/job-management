from datetime import datetime
from decimal import Decimal
import json
import random
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.forms import modelformset_factory
from django.contrib import messages
from app_common.models import User
from .models import EmployeeDetails, Invoice, Quotation, Quotation2, Item
from .forms import EmployeeDetailsForm, InvoiceDetailForm, QuotationForm, QuotationForm2
from .decorators import super_admin_only
from django import forms
from django.db.models import Max
from num2words import num2words

from decimal import Decimal

class ChooseQuotationView(View):
    template_name = 'admin/quotation/choose_quotation.html'
    def get(self, request):
        context = {}
        return render(request, self.template_name, context)
    
class ViewQuotationView(View):
    template_name = 'admin/quotation/view_quotation.html'
    def get(self, request):
        context = {}
        return render(request, self.template_name, context)
    
@method_decorator(super_admin_only, name='dispatch')
class QuotationListView1(View):
    template_name = 'admin/quotation/quotation_list1.html'

    def get(self, request):
        quotations = Quotation.objects.all()
        context = {'quotations': quotations}
        return render(request, self.template_name, context)
    
@method_decorator(super_admin_only, name='dispatch')
class QuotationListView2(View):
    template_name = 'admin/quotation/quotation_list2.html'

    def get(self, request):
        quotations = Quotation2.objects.all()
        context = {'quotations': quotations}
        return render(request, self.template_name, context)

@method_decorator(super_admin_only, name='dispatch')
class QuotationCreateView(View):
    model = Quotation
    form_class = QuotationForm
    template_name = 'admin/quotation/quotation_form1.html'
    def get(self, request):
        context = {
            'form': self.form_class(),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        try:
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Quotation added successfully.")
                return redirect('quotation:quotation_list')
            else:
                messages.error(request, "Form is not valid. Please check the errors.")
                return render(request, self.template_name, {'form': form})
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render(request, error_message, status_code=400)
        
class QuotationCreateView2(View):
    template_name = 'admin/quotation/quotation_form2.html'

    def get(self, request):
        form = QuotationForm2()
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = QuotationForm2(request.POST)
        try:
            if form.is_valid():
                Quotation = form.save()
                
                return redirect('quotation:quotation_list_2')
            else:
                # Re-render the form with validation errors
                context = {
                    'form': form,
                }
                return render(request, self.template_name, context)
        except Exception as e:
            context = {
                'form': form,
                'error': "An error occurred while processing your request. Please try again."
            }
            return render(request, self.template_name, context)

@method_decorator(super_admin_only, name='dispatch')
class QuotationUpdateView(View):
    model = Quotation
    form_class = QuotationForm
    template_name = 'admin/quotation/quotation_form1.html'

    def get(self, request, pk):
        try:
            quotation = get_object_or_404(self.model, pk=pk)
            form = self.form_class(instance=quotation)
            context = {'form': form}
            return render(request, self.template_name, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render(request, error_message, status_code=400)

    def post(self, request, pk):
        try:
            quotation = get_object_or_404(self.model, pk=pk)
            form = self.form_class(request.POST, request.FILES, instance=quotation)

            if form.is_valid():
                form.save()
                messages.success(request, f"{quotation.title} updated successfully.")
                return redirect('quotation:quotation_list')
            else:
                messages.error(request, "Form is not valid. Please check the errors.")
                return render(request, self.template_name, {'form': form})
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render(request, error_message, status_code=400)

@method_decorator(super_admin_only, name='dispatch')
class QuotationDeleteView(View):
    model = Quotation

    def post(self, request, pk):
        try:
            quotation = get_object_or_404(self.model, pk=pk)
            quotation.delete()
            messages.success(request, "Quotation deleted successfully.")
            return redirect('quotation:quotation_list')
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render(request, 'error.html', {'error_message': error_message}, status=400)
        
@method_decorator(super_admin_only, name='dispatch')
class QuotationDeleteView2(View):
    model = Quotation2

    def post(self, request, pk):
        try:
            print(f"PK is : {pk}")
            quotation = get_object_or_404(self.model, pk=pk)
            quotation.delete()
            messages.success(request, "Quotation deleted successfully.")
            return redirect('quotation:quotation_list_2')
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render(request, 'error.html', {'error_message': error_message}, status=400)
        
class QuotationDetailView1(View):
    template_name = 'admin/quotation/quotation_details1.html'

    def get(self, request, pk):
        user_obj = get_object_or_404(User,id = pk)
        quotation = Quotation.objects.filter(client = user_obj)
     
        context = {
            'quotations': quotation,
            "user_obj":user_obj
        }
        return render(request, self.template_name, context)

class QuotationDetailsView2(View):
    template_name = 'admin/quotation/quotation_details2.html'

    def get(self, request, pk): 
        quotation = get_object_or_404(Quotation2, id=pk)

        # Calculate totals and subtotals for semi-skilled and unskilled workers
        semi_skilled_total = quotation.semi_skilled * quotation.semi_skilled_manpower * quotation.working_days
        unskilled_total = quotation.unskilled * quotation.unskilled_manpower * quotation.working_days

        semi_skilled_subtotal = semi_skilled_total + quotation.other_allowances_semi_skilled
        unskilled_subtotal = unskilled_total + quotation.other_allowances_unskilled

        # Percentages for EPF, ESI, Bonus, Leave Encashment, Gratuity
        epf_percent = Decimal('0.13')
        esi_percent = Decimal('0.0325')
        bonus_percent = Decimal('0.0833')
        leave_encashment_percent = Decimal('0.0577')
        gratuity_percent = Decimal('0.0481')

        semi_skilled_epf = round(semi_skilled_subtotal * epf_percent)
        unskilled_epf = round(unskilled_subtotal * epf_percent)

        semi_skilled_esi = round(semi_skilled_subtotal * esi_percent)
        unskilled_esi = round(unskilled_subtotal * esi_percent)

        semi_skilled_bonus = round(semi_skilled_subtotal * bonus_percent)
        unskilled_bonus = round(unskilled_subtotal * bonus_percent)

        semi_skilled_leave_encashment = round(semi_skilled_subtotal * leave_encashment_percent)
        unskilled_leave_encashment = round(unskilled_subtotal * leave_encashment_percent)

        semi_skilled_gratuity = round(semi_skilled_subtotal * gratuity_percent)
        unskilled_gratuity = round(unskilled_subtotal * gratuity_percent)

        # Additional costs (uniform, reliever, operational)
        semi_uniform_cost = quotation.semi_uniform_cost or 0
        un_uniform_cost = quotation.un_uniform_cost or 0
        semi_reliever_cost = quotation.semi_reliever_cost or 0
        un_reliever_cost = quotation.un_reliever_cost or 0
        semi_operational_cost = quotation.semi_operational_cost or 0
        un_operational_cost = quotation.un_operational_cost or 0

        # Total calculations
        semi_skilled_total_cost = semi_skilled_subtotal + semi_skilled_epf + semi_skilled_esi + semi_skilled_bonus + semi_skilled_leave_encashment + semi_skilled_gratuity + semi_uniform_cost + semi_reliever_cost + semi_operational_cost
        unskilled_total_cost = unskilled_subtotal + unskilled_epf + unskilled_esi + unskilled_bonus + unskilled_leave_encashment + unskilled_gratuity + un_uniform_cost + un_reliever_cost + un_operational_cost

        # Service charge
        service_charge_percent = Decimal('0.028')  # Convert to Decimal
        semi_skilled_service_charge = round(semi_skilled_total_cost * service_charge_percent)
        unskilled_service_charge = round(unskilled_total_cost * service_charge_percent)

        # Final totals
        semi_skilled_final_total = semi_skilled_total_cost + semi_skilled_service_charge
        unskilled_final_total = unskilled_total_cost + unskilled_service_charge

        # GST
        gst_percent = Decimal('0.18')  # Convert to Decimal
        semi_skilled_gst = round(semi_skilled_final_total * gst_percent)
        unskilled_gst = round(unskilled_final_total * gst_percent)

        # Total manpower cost
        semi_skilled_total_manpower_cost = semi_skilled_final_total + semi_skilled_gst
        unskilled_total_manpower_cost = unskilled_final_total + unskilled_gst

        # Prepare context
        context = {
            'quotation': quotation,
            'semi_skilled_total': semi_skilled_total,
            'unskilled_total': unskilled_total,
            'semi_skilled_subtotal': semi_skilled_subtotal,
            'unskilled_subtotal': unskilled_subtotal,
            'semi_skilled_epf': semi_skilled_epf,
            'unskilled_epf': unskilled_epf,
            'semi_skilled_esi': semi_skilled_esi,
            'unskilled_esi': unskilled_esi,
            'semi_skilled_bonus': semi_skilled_bonus,
            'unskilled_bonus': unskilled_bonus,
            'semi_skilled_leave_encashment': semi_skilled_leave_encashment,
            'unskilled_leave_encashment': unskilled_leave_encashment,
            'semi_skilled_gratuity': semi_skilled_gratuity,
            'unskilled_gratuity': unskilled_gratuity,
            'semi_uniform_cost': semi_uniform_cost,
            'un_uniform_cost': un_uniform_cost,
            'semi_reliever_cost': semi_reliever_cost,
            'un_reliever_cost': un_reliever_cost,
            'semi_operational_cost': semi_operational_cost,
            'un_operational_cost': un_operational_cost,
            'semi_skilled_total_cost': semi_skilled_total_cost,
            'unskilled_total_cost': unskilled_total_cost,
            'semi_skilled_service_charge': semi_skilled_service_charge,
            'unskilled_service_charge': unskilled_service_charge,
            'semi_skilled_final_total': semi_skilled_final_total,
            'unskilled_final_total': unskilled_final_total,
            'semi_skilled_gst': semi_skilled_gst,
            'unskilled_gst': unskilled_gst,
            'semi_skilled_total_cost_with_gst': semi_skilled_final_total + semi_skilled_gst,
            'unskilled_total_cost_with_gst': unskilled_final_total + unskilled_gst,
            'semi_skilled_total_manpower_cost': semi_skilled_total_manpower_cost,
            'unskilled_total_manpower_cost': unskilled_total_manpower_cost,
        }

        return render(request, self.template_name, context)

class InvoiceDetailCreateView(View):
    template_name = 'admin/quotation/invoice_detail_form.html'
    success_url = reverse_lazy('quotation:invoice_list')

    def get(self, request, *args, **kwargs):
        invoice_form = InvoiceDetailForm()
        return render(request, self.template_name, {
            'invoice_form': invoice_form,
        })

    def post(self, request, *args, **kwargs):
        invoice_form = InvoiceDetailForm(request.POST)
        
        if invoice_form.is_valid():
            # Create and save the Invoice
            invoice = invoice_form.save(commit=False)
            employee_details_list = request.POST.getlist('employee_details')  # Get the JSON string list
            
            if employee_details_list:
                # Assuming employee_details is sent as a JSON string from your JS
                employee_details = json.loads(employee_details_list[0])  # Convert to list of dicts

                # Save employee details as a JSONField in the invoice
                invoice.employee_details = employee_details
            
            invoice.save()
            return redirect(self.success_url)

        return render(request, self.template_name, {
            'invoice_form': invoice_form,
        })
    
class InvoiceListView(View):
    model = Invoice
    template_name = 'admin/quotation/invoice_list.html'
    context_object_name = 'invoices'

    def get_queryset(self):
        return Invoice.objects.all()

    def get(self, request):
        invoices = self.get_queryset()
        context = {
            self.context_object_name: invoices
        }
        return render(request, self.template_name, context)

class InvoiceDetailView(View):
    template_name = 'admin/quotation/invoice.html'  # Adjust the template as necessary

    def get(self, request, *args, **kwargs):
        invoice_id = kwargs.get('invoice_id')  # Assuming you're passing the invoice ID in the URL
        invoice = get_object_or_404(Invoice, invoice_detail_id=invoice_id)

        # Access employee details directly as it is already a list
        employee_details = invoice.employee_details  # No need for json.loads()

        # Calculate subtotal price
        subtotal_price = Decimal(0)
        for employee in employee_details:
            subtotal_price += Decimal(employee.get('total_price', 0))  # Safely get the total price

        # Calculate GST and total amount (if needed)
        gst_percentage = Decimal(18)  # Example static GST percentage
        gst_amount = (subtotal_price * gst_percentage) / Decimal(100)
        total_amount = subtotal_price + gst_amount

        # Prepare the grand total and amount in words
        grand_total_amount = subtotal_price + gst_amount + (invoice.esi or 0) + (invoice.epf or 0)
        grand_total_amount_words = self.convert_to_words(grand_total_amount)

        # Pass the calculated values to the template
        return render(request, self.template_name, {
            'invoice': invoice,
            'employee_details': employee_details,  # Pass employee details to the template
            'subtotal_price': subtotal_price,
            'gst_amount': gst_amount,
            'total_amount': total_amount,
            'grand_total_amount': grand_total_amount,
            'grand_total_amount_words': grand_total_amount_words,
        })

    def convert_to_words(self, amount):
        # Convert the numeric amount into words
        return num2words(amount, to='currency', lang='en')

class InvoiceDeleteView(View):
    model = Invoice

    def post(self, request, pk):
        try:
            invoice = get_object_or_404(self.model, pk=pk)
            invoice.delete()
            messages.success(request, "Invoice deleted successfully.")
            return redirect('quotation:invoice_list')
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render(request, 'error.html', {'error_message': error_message}, status=400)
        
def generate_invoice_number():
    year = datetime.now().strftime('%y-%y')
    number = str(random.randint(1, 999)).zfill(3)
    return f"PR/INVOICE/{year}/{number}"

invoice_number = generate_invoice_number()
created_date = datetime.now().strftime('%Y-%m-%d')