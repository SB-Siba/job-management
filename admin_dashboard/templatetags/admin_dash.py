from django import template
from django.db.models import Count
register = template.Library()

# from app_common.models import Order


@register.simple_tag
def order_data():
    
    order_counts = Order.objects.values('order_status').annotate(count=Count('order_status'))
    print(order_counts)
    for data in order_counts:
        print(data['order_status'], data['count'])
    
@register.simple_tag
def rounda(value):
    try:
        data = float(value)
        return round(data,2)
    except:
        return '0(e)'