from django.db import models

from menus.models import MenuItem
from users.models import User

class CartsQueryset(models.QuerySet):
    def total_price(self):
        return sum(cart.product_price() for cart in self)
    
    def total_quantity(self):
      if self:
          return sum(cart.quantity for cart in self)
      return 0

class Carts(models.Model):
    
    user = models.ForeignKey(to=User,on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')
    product = models.ForeignKey(to=MenuItem,on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveSmallIntegerField(default=0 , verbose_name='Количество')
    session_key = models.CharField(max_length=32, null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        db_table = 'cart'
        verbose_name = 'Корзину'
        verbose_name_plural = 'Корзины'
    
    objects = CartsQueryset().as_manager()
    

    def product_price(self):
        return round(self.product.sell_price() * self.quantity,2) 
    
    def __str__(self):
        if self.user:
            return f" Корзина {self.user.username} | Товар {self.product.name} | Количество {self.quantity}"
      
        return f" Анонимная корзина | Товар {self.product.name} | Количество {self.quantity}"

