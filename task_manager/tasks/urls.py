from django.urls import path

#from django_filters.views import FilterView
#from task_manager.tasks.models import Task
from task_manager.tasks.views import (
    TasksView,
    TaskView,
    TaskViewCreate,
    TaskViewDelete,
    TaskViewUpdate,
)

urlpatterns = [
    path('', TasksView.as_view(), name='tasks_show'),
#    path('', FilterView.as_view(model=Task), name='tasks_show'),
    path('<int:pk>/', TaskView.as_view(), name='task_show'),
    path('create/', TaskViewCreate.as_view(), name='task_create'),
    path('<int:pk>/update/', TaskViewUpdate.as_view(), name='task_update'),
    path('<int:pk>/delete/', TaskViewDelete.as_view(), name='task_delete'),
]
