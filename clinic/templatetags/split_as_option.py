from django import template
from django.utils.safestring import mark_safe, SafeData
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def split_as_option(value, splitter=',', autoescape=None):

    return value.split(splitter)
split_as_option.is_safe = True
split_as_option.needs_autoescape = True