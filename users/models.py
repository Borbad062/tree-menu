from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
  image = models.ImageField(upload_to='users_images', blank=True, null=True, verbose_name='Аватар')

  class Meta:
    db_table = 'users'
    verbose_name = 'Пользователь'
    verbose_name_plural = 'Пользователи'