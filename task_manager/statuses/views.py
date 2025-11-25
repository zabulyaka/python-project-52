from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status


class StatusesView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        statuses = Status.objects.all()
        url = 'statuses/statuses_show.html'
        context = {'statuses': statuses}
        return render(request, url, context)

    def handle_no_permission(self):
        messages.error(
            self.request,
            'Вы не авторизованы! Пожалуйста, выполните вход.'
        )
        return redirect('user_login')


class StatusViewCreate(LoginRequiredMixin, CreateView):
    model = Status
    form = StatusForm
    template_name = 'statuses/status_create.html'
    success_url = reverse_lazy('statuses_show')
    fields = ['name']
    
    def form_valid(self, form):
        messages.success(
            self.request,
            'Статус успешно создан'
        )
        return super().form_valid(form)

    def handle_no_permission(self):
        messages.error(
            self.request,
            'Вы не авторизованы! Пожалуйста, выполните вход.'
        )
        return redirect('user_login')


class StatusViewUpdate(LoginRequiredMixin, UpdateView):
    model = Status
    form = StatusForm
    template_name = 'statuses/status_update.html'
    success_url = reverse_lazy('statuses_show')
    fields = ['name']
    
    def form_valid(self, form):
        messages.success(
            self.request,
            'Статус успешно изменен'
        )
        return super().form_valid(form)

    def handle_no_permission(self):
        messages.error(
            self.request,
            'Вы не авторизованы! Пожалуйста, выполните вход.'
        )
        return redirect('user_login')


class StatusViewDelete(LoginRequiredMixin, DeleteView):
    model = Status
    form = StatusForm
    template_name = 'statuses/status_delete.html'
    success_url = reverse_lazy('statuses_show')
    fields = ['name']
    
    def handle_no_permission(self):
        messages.error(
            self.request,
            'Вы не авторизованы! Пожалуйста, выполните вход.'
        )
        return redirect('user_login')

    def post(self, request, *args, **kwargs):
        try:
            result = super().post(request, *args, **kwargs)
            messages.success(
                self.request,
                'Статус успешно удален'
            )
#            return super().post(request, *args, **kwargs)
            return result
        except ProtectedError:
            messages.error(
                self.request,
                'Невозможно удалить статус, используемый в задаче.'
            )
            return redirect(self.success_url)

