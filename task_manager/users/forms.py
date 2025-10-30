# from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from task_manager.users.models import User


# class UserForm(ModelForm):
class UserFormCreate(UserCreationForm):
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
#class UserFormLogin(AuthenticationForm):
#    pass
