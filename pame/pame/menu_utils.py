# menu_utils.py

from django import template

register = template.Library()

@register.simple_tag
def es_grupo_admin(user):
    return user.groups.filter(name='admin').exists()
