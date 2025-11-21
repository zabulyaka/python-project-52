from django.db import models

from task_manager.users.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


class Task(models.Model):
    name = models.CharField(max_length=150, verbose_name='Имя', unique=True)
    description = models.TextField(max_length=300, verbose_name='Описание', blank=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='authored_tasks', verbose_name='Автор')
    executor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='executed_tasks', verbose_name='Исполнитель', blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name='Статус')
    labels = models.ManyToManyField(Label, verbose_name='Метки', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'


# Create your models here.
