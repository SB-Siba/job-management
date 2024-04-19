from django import template
register = template.Library()

@register.simple_tag
def new_complaints(dist_object):
    return None
