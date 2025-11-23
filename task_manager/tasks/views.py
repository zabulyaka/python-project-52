from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django_filters.views import FilterView

from task_manager.tasks.forms import TaskForm, TaskFilter
from task_manager.tasks.models import Task


class TasksView(LoginRequiredMixin, FilterView):
    model = Task
    filterset_class = TaskFilter
    template_name = 'tasks/tasks_show.html'
#    template_name = 'tasks/task_filter.html'
    context_object_name = 'tasks'

    def handle_no_permission(self):
        messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return redirect('user_login')
#class TasksView(LoginRequiredMixin, View):
#    def get(self, request, *args, **kwargs):
#        tasks = Task.objects.all()
#        url = 'tasks/tasks_show.html'
#        context = {'tasks': tasks}
#        return render(request, url, context)

#    def handle_no_permission(self):
#        messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
#        return redirect('user_login')

class TaskView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        task = Task.objects.get(pk=kwargs['pk'])
        url = 'tasks/task_show.html'
        context = {'task': task}
        return render(request, url, context)

    def handle_no_permission(self):
        messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return redirect('user_login')


class TaskViewCreate(LoginRequiredMixin, CreateView):
    model = Task
    form = TaskForm
    template_name = 'tasks/task_create.html'
    success_url = reverse_lazy('tasks_show')
    fields = ['name', 'description', 'executor', 'status', 'labels']
    
    def form_valid(self, form):
        messages.success(self.request, 'Задача успешно создана')
        form.instance.author = self.request.user
        return super().form_valid(form)

    def handle_no_permission(self):
        messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return redirect('user_login')


class TaskViewUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    form = TaskForm
    template_name = 'tasks/task_update.html'
    success_url = reverse_lazy('tasks_show')
    fields = ['name', 'description', 'executor', 'status', 'labels']
    
    def form_valid(self, form):
        messages.success(self.request, 'Задача успешно изменена')
        return super().form_valid(form)

    def handle_no_permission(self):
        messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return redirect('user_login')


class TaskViewDelete(LoginRequiredMixin, DeleteView):
    model = Task
    form = TaskForm
    template_name = 'tasks/task_delete.html'
    success_url = reverse_lazy('tasks_show')
    fields = ['name']
    
    def form_valid(self, form):
        messages.success(self.request, 'Задача успешно удалена')
        return super().form_valid(form)

    def handle_no_permission(self):
        messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return redirect('user_login')
