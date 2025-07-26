from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView

from menus.models import Menu, MenuItem
from .utils import q_search

class MenuView(ListView):
  # model = MenuItem
  queryset = MenuItem.objects.filter().order_by("id")
  template_name = 'menus/menu.html'
  slug_url_kwarg = "menu_slug"
  context_object_name = "menus"
  paginate_by = 3

  

  def get_queryset(self):
    menu_slug = self.kwargs.get(self.slug_url_kwarg)
    on_sale = self.request.GET.get('on_sale')
    order_by = self.request.GET.get('order_by')
    query = self.request.GET.get('q')

    if menu_slug == 'all':
      menus = super().get_queryset()
    elif query:
      menus = q_search(query)
    else:
      menus = MenuItem.objects.filter(menu__slug=menu_slug)
    
    if on_sale:
      menus = menus.filter(discount__gt=0)
    if order_by and order_by != "default":
      menus = menus.order_by(order_by)
    
    return menus

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["title"] = 'Home - каталог'
      context["slug_url"] = self.kwargs.get(self.slug_url_kwarg)
      return context  
      


class MenuItemView(DetailView):

  template_name = "menus/menuitem.html"
  slug_url_kwarg = 'product_slug'
  context_object_name = "product"

  def get_object(self, queryset=None):
    product = MenuItem.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
    return product
  

  def get_context_data(self, **kwargs):
    context =  super().get_context_data(**kwargs)
    context["title"] = 'Товар'
    return context

