from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=200, verbose_name='Имя пользователя', help_text='Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.')
    first_name = models.CharField(max_length=200, verbose_name='Имя')
    last_name = models.CharField(max_length=200, verbose_name='Фамилия')
    password1 = models.CharField(max_length=200, verbose_name='Пароль', help_text='Ваш пароль должен содержать как минимум 3 символа.')
    password2 = models.CharField(max_length=200, verbose_name='Подтверждение пароля', help_text='Для подтверждения введите, пожалуйста, пароль ещё раз.')
    created_at = models.DateTimeField(auto_now_add=True)
