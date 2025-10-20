# from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from task_manager.users.models import User


# class UserForm(ModelForm):
class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2"
        ]

class UserFormLogin(AuthenticationForm):
    pass
