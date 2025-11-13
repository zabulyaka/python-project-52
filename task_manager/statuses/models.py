from django.db import models

class Status(models.Model):
    name = models.CharField(max_length=150, verbose_name='Имя', unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'
# Create your models here.
