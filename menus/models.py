from django.db import models

class Menu(models.Model):
  name = models.CharField(max_length=150, unique=True, verbose_name='Название')
  slug = models.CharField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

  class Meta:
    db_table = 'menu'
    verbose_name= 'Меню'
    verbose_name_plural = 'Меню'
  
  def __str__(self):
     return self.name

class MenuItem(models.Model):
  name = models.CharField(max_length=150, unique=True, verbose_name='Название')
  slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
  description = models.TextField(blank=True, null=True, verbose_name='Описание')
  image = models.ImageField(upload_to='menus_images', blank=True, null=True, verbose_name='Изображение')
  price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Цена')
  discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=2, verbose_name='Скидка в %')
  quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
  menu = models.ForeignKey(to=Menu, on_delete=models.CASCADE, verbose_name='Меню')
 
  class Meta:
        db_table = 'menuitem'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-image']
  
  def __str__(self):
    return self.name
  
  def display_id(self):
     return f"{self.pk:05}"
  
  def sell_price(self):
     if self.discount:
        return round(self.price - self.price * (self.discount / 100), 2)
     return self.price