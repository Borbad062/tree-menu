from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views import View

from carts.models import Carts
from menus.models import MenuItem


class CartAddView(View):
  def post(self, request):
    product_id = request.POST.get("product_id")
    product = MenuItem.objects.get(id=product_id)

    if request.user.is_authenticated:
        carts = Carts.objects.filter(user=request.user, product=product)

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Carts.objects.create(user=request.user, product=product, quantity=1)

    else:
        carts = Carts.objects.filter(
            session_key=request.session.session_key, product=product)

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Carts.objects.create(
                session_key=request.session.session_key, product=product, quantity=1)
        
    
    cart_items_html = render_to_string(
      "carts/includes/included_carts.html", request=request
    )

    response_data = {
      "message": "Товар добавлен в корзину",
      "cart_items_html":cart_items_html
    }

    return JsonResponse(response_data)


class CartChangeView(View):
    def post(self, request):
        
        cart_id = request.POST.get("cart_id")
        
        cart = Carts.objects.get(id=cart_id)

        cart.quantity = request.POST.get("quantity")
        cart.save()

        quantity = cart.quantity
        cart_items_html = render_to_string(
          "carts/includes/included_carts.html", request=request)

        response_data = {
            "message": "Количество изменено",
            "quantity": quantity,
            'cart_items_html': cart_items_html
        }

        return JsonResponse(response_data)


class CartRemoveView(View):
  def post(self, request):
    cart_id =  request.POST.get('cart_id')

    cart = Carts.objects.get(id=cart_id)
    quantity = cart.quantity
    cart.delete()

    cart_items_html = render_to_string(
      "carts/includes/included_carts.html", request=request
    )

    response_data = {
            "message": "Товар удален из корзины",
            "quantity_deleted": quantity,
            'cart_items_html': cart_items_html
        }

    return JsonResponse(response_data)
    