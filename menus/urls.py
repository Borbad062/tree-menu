from django.urls import path
from .views import  MenuItemView, MenuView

app_name = 'menus'

urlpatterns = [
    path('search/', MenuView.as_view(), name='search'),
    path('<slug:menu_slug>/', MenuView.as_view(), name='index'),
    path('product/<slug:product_slug>/', MenuItemView.as_view(), name='product'),
]
