from django import template
import base64

register = template.Library()

@register.simple_tag
def base64_encode(value):
    if value:
        return base64.b64encode(value).decode('utf-8')
    return ''