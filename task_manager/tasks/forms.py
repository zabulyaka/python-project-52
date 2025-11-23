from django.forms import ModelForm, SelectMultiple, CheckboxInput
from django_filters import FilterSet, ModelChoiceFilter, BooleanFilter
#from django.db import models

from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.users.models import User
from task_manager.labels.models import Label


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'executor', 'labels']
        widgets = {'labels': SelectMultiple(attrs={'class': 'form-select'})}


class TaskFilter(FilterSet):
#    name = CharFilter(lookup_expr='iexact')
    status = ModelChoiceFilter(queryset=Status.objects.all(), label='Статус')
    executor = ModelChoiceFilter(queryset=User.objects.all(), label='Исполнитель')
    labels = ModelChoiceFilter(queryset=Label.objects.all(), label='Метки')
    own_tasks = BooleanFilter(method='filter_own_tasks', label='Только свои задачи', widget=CheckboxInput)

    def filter_own_tasks(self, queryset, name, value):
        return queryset.filter(author=self.request.user) if value else queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'own_tasks']
#        widgets = {'own_tasks': CheckboxInput(attrs={'class': 'form-check-input'})}
#        filter_overrides = {
#            models.BooleanField: {
#                'filter_class': BooleanFilter,
#                'extra': lambda f: {
#                    'widget': CheckboxInput(attrs={
#                        'class': 'form-check-input mr-3',
#                        'type': 'checkbox',
#                    }),
#                },
#            },
#        }
#    @property
#    def qs(self):
#        parent = super().qs
#        user = getattr(self.request, 'user', None)
#        self_tasks = getattr(self.request, 'self_tasks', None)
#
#        return parent.filter(author=user) if self_tasks == 'on' else parent
#        return parent.filter(executor='nick')
