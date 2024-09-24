from datetime import datetime
from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.forms import modelformset_factory
from django.contrib import messages
from app_common.models import User
from .models import Quotation, Invoice, Item
from .forms import QuotationForm, CreateInvoiceForm
from .decorators import super_admin_only
from django import forms
from django.db.models import Max


@method_decorator(super_admin_only, name='dispatch')
class QuotationListView(View):
    template_name = 'admin/quotation/quotation_list.html'

    def get(self, request):
        quotations = Quotation.objects.all()
        context = {'quotations': quotations}
        return render(request, self.template_name, context)

class QuotationDetailsView(View):
    def get(self, request, *args, **kwargs):
        quotation_id = kwargs.get('id')
        try:
            quotation = Quotation.objects.get(id=quotation_id)
            data = {
                'id': quotation_id,
                'job_title': quotation.job_title,
                'number_of_persons': quotation.number_of_persons,
                'experience_level': quotation.experience_level,
                'salary': quotation.salary,
                'created_at': quotation.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
            return JsonResponse(data)
        except Quotation.DoesNotExist:
            return JsonResponse({'error': 'Quotation not found'}, status=404)
        
ItemFormSet = modelformset_factory(
    Item,
    fields=('component', 'percentage', 'supervisor', 'gda'),
    extra=1,
    can_delete=True
)

@method_decorator(super_admin_only, name='dispatch')
class QuotationCreateView(View):
    model = Quotation
    form_class = QuotationForm
    template_name = 'admin/quotation/quotation_form.html'
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

@method_decorator(super_admin_only, name='dispatch')
class QuotationUpdateView(View):
    model = Quotation
    form_class = QuotationForm
    template_name = 'admin/quotation/quotation_form.html'

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
        
class QuotationDetailView(View):
    template_name = 'admin/quotation/quotation_details.html'

    def get(self, request, pk):
        user_obj = get_object_or_404(User,id = pk)
        quotation = Quotation.objects.filter(client = user_obj)
     
        context = {
            'quotations': quotation,
            "user_obj":user_obj
        }
        return render(request, self.template_name, context)

class CreateInvoiceView(View):
    template_name = 'admin/quotation/create_invoice.html'

    def get(self, request):
        form = CreateInvoiceForm()
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = CreateInvoiceForm(request.POST)
        try:
            if form.is_valid():

                invoice = form.save()

                return redirect('quotation:invoice', invoice_id=invoice.id)
            else:
                context = {
                'form': form,
            }
            return render(request, self.template_name, context)
        except Exception as e:
            print(e)

from decimal import Decimal

class InvoiceView(View):
    template_name = 'admin/quotation/invoice.html'

    def get(self, request, invoice_id):
        # Fetch the invoice object
        invoice = get_object_or_404(Invoice, id=invoice_id)
        print(invoice.notification_text)

        # Get the current date
        current_date = datetime.now()
        current_year = current_date.year
        current_month = current_date.month

        # Determine the fiscal year range
        if current_month <= 3:
            invoice_year_start = str(current_year)[2:]  # Last two digits of the current year
            invoice_year_end = str(current_year + 1)[2:]  # Last two digits of the next year
        else:
            invoice_year_start = str(current_year)[2:]  # Last two digits of the current year
            invoice_year_end = str(current_year + 1)[2:]  # Last two digits of the next year

        # Generate the serial number for the invoice
        last_invoice = Invoice.objects.all().aggregate(Max('id'))
        new_serial_number = last_invoice['id__max'] + 1 if last_invoice['id__max'] else 1

        # Create the invoice ID
        invoice_id_str = f"PR/INVOICE/{invoice_year_start}-{invoice_year_end}/{str(new_serial_number).zfill(3)}"

        # Calculate totals and percentages
        semi_skilled_total = invoice.semi_skilled * invoice.semi_skilled_manpower * invoice.working_days
        unskilled_total = invoice.unskilled * invoice.unskilled_manpower * invoice.working_days

        semi_skilled_subtotal = semi_skilled_total + invoice.other_allowances_semi_skilled
        unskilled_subtotal = unskilled_total + invoice.other_allowances_unskilled

        # EPF, ESI, Bonus, Leave Encashment, Gratuity percentages
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

        # Costs
        semi_uniform_cost = invoice.semi_uniform_cost or 0
        un_uniform_cost = invoice.un_uniform_cost or 0
        semi_reliever_cost = invoice.semi_reliever_cost or 0
        un_reliever_cost = invoice.un_reliever_cost or 0
        semi_operational_cost = invoice.semi_operational_cost or 0
        un_operational_cost = invoice.un_operational_cost or 0

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
        total_manpower_cost = semi_skilled_final_total + unskilled_final_total + semi_skilled_gst + unskilled_gst

        # Prepare context
        context = {
            'invoice': invoice,
            'invoice_id': invoice_id_str,
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
            'total_manpower_cost': total_manpower_cost,
            'semi_skilled_total_cost_with_gst': semi_skilled_final_total + semi_skilled_gst,
            'unskilled_total_cost_with_gst': unskilled_final_total + unskilled_gst,
        }

        return render(request, self.template_name, context)