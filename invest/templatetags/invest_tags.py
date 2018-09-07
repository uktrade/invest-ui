from django import template
from django.template.defaultfilters import stringfilter
from django.utils import translation


register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def title_from_heading(value):
    if translation.get_language_bidi():
        return value.split(':')[1].strip()
    return value.split(':')[0].strip()
