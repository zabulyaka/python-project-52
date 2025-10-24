from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    username = models.CharField(max_length=200, verbose_name='Имя пользователя', help_text='Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.', unique=True)
    first_name = models.CharField(max_length=200, verbose_name='Имя')
    last_name = models.CharField(max_length=200, verbose_name='Фамилия')

