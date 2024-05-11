from celery import shared_task
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import get_template
from . models import UserSubscription
# from app_common.checkout.serializer import OrderSerializer

@shared_task
def send_forgot_password_link(user_id ,email, otp):
    html_tpl_path = 'app_common/authentication/forgot_password_email_template.html'

    encoded_user_id= urlsafe_base64_encode(str(user_id).encode('utf-8'))


    url=settings.DOMAIN_NAME+'new_password_set/{}/{}'.format(encoded_user_id, otp)

    context={
        "reciver_email":email,
        "url": url
    }
    email_html_template = get_template(html_tpl_path).render(context)

    subject = 'Forgot Password - LakshmiMart'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email,]
    email_msg=EmailMessage( subject, email_html_template, email_from, recipient_list )
    email_msg.content_subtype = 'html'

    
    try:
        email_msg.send(fail_silently=False)
    except Exception as e:
        print("#############################################")
        print(str(e))
        print("#############################################")




@shared_task
def share_invoice(email,data):

    html_tpl_path = 'app_common/checkout/invoice.html'


    for product in data['products']:
        product['product']['quantity']=product['quantity']

    context ={
        'order':data,
        'address':data['address'],
        'product_list':data['products'],
        'charges':data['order_meta_data']['charges'],
        'gross_amt':data['order_meta_data']['our_price'],
        'discount':data['order_meta_data']['our_price'] - data['order_value'],
    }
    email_html_template = get_template(html_tpl_path).render(context)

    subject = 'Invoice - LakshmiMart'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, 'lakshmimart.tapas@gmail.com',]
    email_msg=EmailMessage( subject, email_html_template, email_from, recipient_list )
    email_msg.content_subtype = 'html'

    
    try:
        email_msg.send(fail_silently=False)
    except Exception as e:
        print("#############################################")
        print(str(e))
        print("#############################################")

@shared_task
def renew_subscription(subscription_id):
    subscription = UserSubscription.objects.get(id=subscription_id)
    new_end_date = subscription.auto_renew()
    return new_end_date