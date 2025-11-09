from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from task_manager.users.forms import UserFormCreate, UserFormUpdate, UserFormLogin
from task_manager.users.models import User


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
    template_name = 'users/user_create.html'
    success_url = reverse_lazy('user_login')
    form_class = UserFormCreate
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, 'Пользователь успешно зарегистрирован')
        return super().form_valid(form)


class UserViewUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('users_show')
    form_class = UserFormUpdate
    login_url = reverse_lazy('user_login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Редактирование пользователя прошло успешно')
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
            messages.error(self.request, 'У вас нет прав для удаления другого пользователя.')
            return redirect('users_show')
        else:
            messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect('user_login')


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
    

