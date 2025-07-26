
from django import template

from carts.models import Carts


register = template.Library()

@register.simple_tag()
def user_tags(request):
  if request.user.is_authenticated:
    return Carts.objects.filter(user=request.user).select_related('product')
  
  if not request.session.session_key:
    return request.session.create()
  return Carts.objects.filter(session_key=request.session.session_key).select_related('product')