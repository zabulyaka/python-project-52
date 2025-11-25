from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label


class LabelsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        labels = Label.objects.all()
        url = 'labels/labels_show.html'
        context = {'labels': labels}
        return render(request, url, context)

    def handle_no_permission(self):
        messages.error(
            self.request,
            'Вы не авторизованы! Пожалуйста, выполните вход.'
        )
        return redirect('user_login')


class LabelViewCreate(LoginRequiredMixin, CreateView):
    model = Label
    form = LabelForm
    template_name = 'labels/label_create.html'
    success_url = reverse_lazy('labels_show')
    fields = ['name']
    
    def form_valid(self, form):
        messages.success(
            self.request,
            'Метка успешно создана'
        )
        return super().form_valid(form)

    def handle_no_permission(self):
        messages.error(
            self.request,
            'Вы не авторизованы! Пожалуйста, выполните вход.'
        )
        return redirect('user_login')


class LabelViewUpdate(LoginRequiredMixin, UpdateView):
    model = Label
    form = LabelForm
    template_name = 'labels/label_update.html'
    success_url = reverse_lazy('labels_show')
    fields = ['name']
    
    def form_valid(self, form):
        messages.success(
            self.request,
            'Метка успешно изменена'
        )
        return super().form_valid(form)

    def handle_no_permission(self):
        messages.error(
            self.request,
            'Вы не авторизованы! Пожалуйста, выполните вход.'
        )
        return redirect('user_login')


class LabelViewDelete(LoginRequiredMixin, DeleteView):
    model = Label
    form = LabelForm
    template_name = 'labels/label_delete.html'
    success_url = reverse_lazy('labels_show')
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
                'Метка успешно удалена'
            )
            return result
#            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                self.request,
                'Невозможно удалить метку, используемую в задаче.'
            )
            return redirect(self.success_url)
