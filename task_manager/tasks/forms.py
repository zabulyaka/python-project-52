from django.forms import CheckboxInput, ModelForm, SelectMultiple
from django_filters import BooleanFilter, FilterSet, ModelChoiceFilter

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'executor', 'labels']
        widgets = {'labels': SelectMultiple(attrs={'class': 'form-select'})}


class TaskFilter(FilterSet):
    status = ModelChoiceFilter(queryset=Status.objects.all(), label='Статус')
    executor = ModelChoiceFilter(
        queryset=User.objects.all(),
        label='Исполнитель'
    )
    labels = ModelChoiceFilter(queryset=Label.objects.all(), label='Метка')
    own_tasks = BooleanFilter(
        method='filter_own_tasks',
        label='Только свои задачи',
        widget=CheckboxInput
    )

    def filter_own_tasks(self, queryset, name, value):
        return queryset.filter(author=self.request.user) if value else queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'own_tasks']

