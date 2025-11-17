from django.forms import ModelForm, SelectMultiple

from task_manager.tasks.models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'author', 'executor', 'labels']
        widgets = {'labels': SelectMultiple(attrs={'class': 'form-select'})}
