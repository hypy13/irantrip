from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='split')
def split(value, separator):
    return value.split(separator)


@register.simple_tag(takes_context=True)
def is_active_page(context, name):
    try:
        if context['request'].resolver_match.url_name == name:
            return "current-item"
    except Exception:
        return ''
