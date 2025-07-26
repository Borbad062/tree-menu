from django.contrib import admin
from .models import Menu, MenuItem

# admin.site.register(Menu)
# admin.site.register(MenuItem)

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug':('name',)}

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug':('name',)}