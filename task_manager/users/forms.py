from django.contrib.auth.password_validation import validate_password, password_changed
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from task_manager.users.models import User


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
        ]


class UserFormUpdate(UserChangeForm):
    password1 = forms.CharField(
        label='Пароль',
        help_text='Ваш пароль должен содержать как минимум 3 символа.',
        widget=forms.PasswordInput,
        initial='',
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        help_text='Для подтверждения введите, пожалуйста, пароль ещё раз.',
        widget=forms.PasswordInput,
        initial='',
    )
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        if password1:
            try:
                validate_password(password1)
            except ValidationError:
                self.add_error('password1','Пароль не удовлетворяет требованиям')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password2 != password1:
            self.add_error('password2', 'Пароли не совпадают')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')
        user.set_password(password)
        password_changed(password, self.instance)
        if commit:
            user.save()
        return user


class UserFormLogin(AuthenticationForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

