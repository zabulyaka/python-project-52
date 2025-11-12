from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
        help_text='Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.',
        unique=True, 
        error_messages={'unique': 'Имя пользователя должно быть уникальным.'}
    )
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.username}'
