from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import ProtectedError

from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status


class StatusesView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        statuses = Status.objects.all()
        url = 'statuses/statuses_show.html'
        context = {'statuses': statuses}
        return render(request, url, context)

    def handle_no_permission(self):
        messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return redirect('user_login')


class StatusViewCreate(LoginRequiredMixin, CreateView):
    model = Status
    form = StatusForm
    template_name = 'statuses/status_create.html'
    success_url = reverse_lazy('statuses_show')
    fields = ['name']
    
    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно создан')
        return super().form_valid(form)

    def handle_no_permission(self):
        messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return redirect('user_login')


class StatusViewUpdate(LoginRequiredMixin, UpdateView):
    model = Status
    form = StatusForm
    template_name = 'statuses/status_update.html'
    success_url = reverse_lazy('statuses_show')
    fields = ['name']
    
    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно изменен')
        return super().form_valid(form)

    def handle_no_permission(self):
        messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return redirect('user_login')


class StatusViewDelete(LoginRequiredMixin, DeleteView):
    model = Status
    form = StatusForm
    template_name = 'statuses/status_delete.html'
    success_url = reverse_lazy('statuses_show')
    fields = ['name']
    
#    def form_valid(self, form):
#        messages.success(self.request, 'Статус успешно удалён')
#        return super().form_valid(form)

    def handle_no_permission(self):
        messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return redirect('user_login')

    def post(self, request, *args, **kwargs):
        try:
            messages.success(self.request, 'Статус успешно удален')
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(self.request, 'Вы не можете удалить используемый статус.')
            return redirect(self.success_url)
#class StatusViewCreate(LoginRequiredMixin, View):
#    def get(self, request, *args, **kwargs):
#        form = StatusForm()
#        url = 'statuses/status_create.html'
#        context = {'form': form}
#        return render(request, url, context)
#
#    def post(self, request, *args, **kwargs):
#        form = StatusForm(request.POST)
#        url = 'statuses/status_create.html'
#        context = {'form': form}
#        if form.is_valid():
#            messages.success(request, 'Статус успешно создан')
#            status = Status(name=form.cleaned_data['name'])
#            status.save()
#            return redirect('statuses_show')
#        return render(request, url, context)
#
#    def handle_no_permission(self):
#        messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
#        return redirect('user_login')


#class StatusViewUpdate(LoginRequiredMixin, View):
#    def get(self, request, *args, **kwargs):
#        status_pk = kwargs.get('pk')
#        status = Status.objects.get(pk=status_pk)
#        form = StatusForm(instance=status)
#        url = 'statuses/status_update.html'
#        context = {'form': form, 'status': status}
#        return render(request, url, context)

#    def post(self, request, *args, **kwargs):
#        status_pk = kwargs.get('pk')
#        status = Status.objects.get(pk=status_pk)
#        form = StatusForm(request.POST, instance=status)
#        url = 'statuses/status_update.html'
#        context = {'form': form, 'status': status}
#        if form.is_valid():
#            messages.success(request, 'Статус успешно изменён')
#            form.save()
#            return redirect('statuses_show')
#        return render(request, url, context)

#    def handle_no_permission(self):
#        messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
#        return redirect('user_login')


#class StatusViewDelete(LoginRequiredMixin, View):
#    def get(self, request, *args, **kwargs):
#        status_pk = kwargs.get('pk')
#        status = Status.objects.get(pk=status_pk)
#        url = 'statuses/status_delete.html'
#        context = {'status': status}
#        return render(request, url, context)

#    def post(self, request, *args, **kwargs):
#        status_pk = kwargs.get('pk')
#        status = Status.objects.get(pk=status_pk)
#        if status:
#            messages.success(request, 'Статус успешно удалён')
#            status.delete()
#        return redirect('statuses_show')

#    def handle_no_permission(self):
#        messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
#        return redirect('user_login')

