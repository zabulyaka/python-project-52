from django.shortcuts import redirect, render
from django.views import View

from task_manager.users.forms import UserForm
from task_manager.users.models import User

# from django.http import HttpResponse
# Create your views here.

# def index(request):
#   return render(request, 'users/show.html', {})
#    return HttpResponse('users')


class UsersView(View):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(
            request,
            'users/show.html',
            context={
                'users': users
            },
        )


class UserViewCreate(View):
    def get(self, request, *args, **kwargs):
        form = UserForm()
        return render(
            request,
            'users/create.html',
            {'form': form},
        )

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            user = User(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                nickname=form.cleaned_data['nickname'],
            )
            user.save()
            return redirect('users_show')
        return render(
            request,
            'users/create.html',
            {'form': form},
        )

class UserViewUpdate(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        form = UserForm(instance=user)
        return render(
            request,
            'users/update.html',
            {'form': form, 'user_id': user_id},
        )

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users_show')
        return render(
            request,
            'users/update.html',
            {'form': form, 'user_id': user_id},
        )

class UserViewDelete(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        return render(
            request,
            'users/delete.html',
            {'user_id': user_id},
        )

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        if user:
            user.delete()
        return redirect('users_show')
