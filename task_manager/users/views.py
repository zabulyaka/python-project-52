from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login

from task_manager.users.forms import UserFormCreate, UserFormUpdate
#from django.contrib.auth.forms import AuthenticationForm
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
            'users/users_show.html',
            {'users': users},
        )


class UserViewCreate(CreateView):
#    model = User
#    fields = ['first_name', 'last_name', 'username', 'password1', 'password2']
#    template_name_suffix = '_create'
    template_name = 'users/user_create.html'
    success_url = reverse_lazy('users_show')
    form_class = UserFormCreate
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

class UserViewUpdate(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'username']
    template_name_suffix = '_update'
    success_url = reverse_lazy('users_show')
    

class UserViewDelete(DeleteView):
    model = User
    fields = ['username']
    template_name_suffix = '_delete'
    success_url = reverse_lazy('users_show')
#class UserViewCreate(View):
#    def get(self, request, *args, **kwargs):
#        form = UserForm()
#        return render(
#            request,
#            'users/create.html',
#            {'form': form},
#        )
#
#    def post(self, request, *args, **kwargs):
#        form = UserForm(request.POST)
#        if form.is_valid():
#            user = User(
#                first_name=form.cleaned_data['first_name'],
#                last_name=form.cleaned_data['last_name'],
#                username=form.cleaned_data['username'],
#            )
#            user.save()
#            return redirect('user_login')
#        return render(
#            request,
#            'users/create.html',
#            {'form': form},
#        )

#class UserViewUpdate(View):
#    def get(self, request, *args, **kwargs):
#        user_id = kwargs.get('id')
#        user = User.objects.get(id=user_id)
#        form = UserForm(instance=user)
#        return render(
#            request,
#            'users/update.html',
#            {'form': form, 'user_id': user_id},
#        )
#
#    def post(self, request, *args, **kwargs):
#        user_id = kwargs.get('id')
#        user = User.objects.get(id=user_id)
#        form = UserForm(request.POST, instance=user)
#        if form.is_valid():
#            form.save()
#            return redirect('users_show')
#        return render(
#            request,
#            'users/update.html',
#            {'form': form, 'user_id': user_id},
#        )

#class UserViewDelete(View):
#    def get(self, request, *args, **kwargs):
#        user_id = kwargs.get('id')
#        return render(
#            request,
#            'users/delete.html',
#            {'user_id': user_id},
#        )
#
#    def post(self, request, *args, **kwargs):
#        user_id = kwargs.get('id')
#        user = User.objects.get(id=user_id)
#        if user:
#            user.delete()
#        return redirect('users_show')

class UserViewLogin(LoginView):
    template_name = 'users/user_login.html'
    

class UserViewLogout(LogoutView):
    pass

