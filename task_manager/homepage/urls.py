from django.urls import path

from task_manager.homepage import views

urlpatterns = [
    path('', views.index, name='index'),
]
