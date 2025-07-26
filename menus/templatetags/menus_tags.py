
from django import template
from django.utils.http import urlencode

from menus.models import Menu


register = template.Library()

@register.simple_tag()
def draw_menu():
  return Menu.objects.all()

@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
  query = context['request'].GET.dict()
  query.update(kwargs)
  return urlencode(query)