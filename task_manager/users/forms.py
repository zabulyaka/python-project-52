# from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from task_manager.users.models import User


# class UserForm(ModelForm):
class UserFormCreate(UserCreationForm):
    password1 = forms.CharField(
        label='Пароль',
        help_text='Ваш пароль должен содержать как минимум 3 символа.',
        widget=forms.PasswordInput,
        initial=''
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        help_text='Для подтверждения введите, пожалуйста, пароль ещё раз.',
        widget=forms.PasswordInput,
        initial=''
    )
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2'
        ]

class UserFormUpdate(UserChangeForm):
    password1 = forms.CharField(
        label='Пароль',
        help_text='Ваш пароль должен содержать как минимум 3 символа.',
        widget=forms.PasswordInput,
        initial=''
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        help_text='Для подтверждения введите, пожалуйста, пароль ещё раз.',
        widget=forms.PasswordInput,
        initial=''
    )
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password')

class UserFormLogin(AuthenticationForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

