from django.urls import path

from task_manager.statuses.views import (
    StatusesView,
    StatusViewCreate,
    StatusViewDelete,
    StatusViewUpdate,
)

urlpatterns = [
    path('', StatusesView.as_view(), name='statuses_show'),
    path('create/', StatusViewCreate.as_view(), name='status_create'),
    path('<int:pk>/update/', StatusViewUpdate.as_view(), name='status_update'),
    path('<int:pk>/delete/', StatusViewDelete.as_view(), name='status_delete'),
]
