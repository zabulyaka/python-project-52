from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login

from task_manager.users.forms import UserFormCreate, UserFormUpdate, UserFormLogin
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
    model = User
#    fields = ['first_name', 'last_name', 'username', 'password1', 'password2']
#    template_name_suffix = '_create'
    template_name = 'users/user_create.html'
    success_url = reverse_lazy('user_login')
    form_class = UserFormCreate
    redirect_authenticated_user = True

    def form_valid(self, form):
#        user = form.save()
        messages.success(self.request, 'Пользователь успешно зарегистрирован')
#        if user is not None:
#            login(self.request, user)
        return super().form_valid(form)

class UserViewUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
#    fields = ['first_name', 'last_name', 'username']
#    template_name_suffix = '_update'
#    success_url = reverse_lazy('users_show')
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('users_show')
    form_class = UserFormUpdate
    login_url = reverse_lazy('user_login')
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            password = form.cleaned_data.get('password1', None)
            password_confirm = form.cleaned_data.get('password2', None)
            if password is not None and password == password_confirm:
                try: 
                    validate_password(password)
                    user.set_password(password)
                    messages.success(self.request, 'Редактирование пользователя прошло успешно')
                except:
                    messages.error(self.request, 'Пароль не удовлетворяет требованиям')
                    return redirect('user_update', user.id)
                finally:
                    login(self.request, user)
            else:
                messages.error(self.request, 'Пароли не совпадают, либо отсутствуют')
                return redirect('user_update', user.id)
#        messages.success(self.request, 'Редактирование пользователя прошло успешно')
        return super().form_valid(form)

    def test_func(self):
        user = self.get_object()
        return self.request.user == user
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'У вас нет прав для изменения другого пользователя.')
            return redirect('users_show')
        else:
            messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect('user_login')

    

class UserViewDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    fields = ['username']
#    template_name_suffix = '_delete'
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('users_show')

    def form_valid(self, form):
        messages.success(self.request, 'Удаление пользователя прошло успешно')
        return super().form_valid(form)

    def test_func(self):
        user = self.get_object()
        return self.request.user == user

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'У вас нет прав для изменения другого пользователя.')
            return redirect('users_show')
        else:
            messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect('user_login')
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
    form_class = UserFormLogin

    def form_valid(self, form):
        messages.success(self.request, 'Вы залогинены')
        return super().form_valid(form)
    

class UserViewLogout(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.info(self.request, 'Вы разлогинены')
        return super().dispatch(request, *args, **kwargs)
    

