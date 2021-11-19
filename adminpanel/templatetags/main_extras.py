
from django import template
register = template.Library()

@register.filter
def in_company(obj, company):
    if obj in company.tags.all():
        return True
    return False