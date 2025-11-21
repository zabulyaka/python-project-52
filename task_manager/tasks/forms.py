from django.forms import ModelForm, SelectMultiple
from django_filters import FilterSet, CharFilter, BooleanFilter

from task_manager.tasks.models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'author', 'executor', 'labels']
        widgets = {'labels': SelectMultiple(attrs={'class': 'form-select'})}


class TaskFilter(FilterSet):
    name = CharFilter(lookup_expr='iexact')

    class Meta:
        model = Task
        fields = ['executor', 'labels']

    @property
    def qs(self):
        parent = super().qs
        user = getattr(self.request, 'user', None)
        self_tasks = getattr(self.request, 'self_tasks', None)

#        return parent.filter(author=user) if self_tasks == 'on' else parent
        return parent.filter(executor='nick')
