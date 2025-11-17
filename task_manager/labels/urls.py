from django.urls import path

from task_manager.labels.views import (
    LabelsView,
    LabelViewCreate,
    LabelViewDelete,
    LabelViewUpdate,
)

urlpatterns = [
    path('', LabelsView.as_view(), name='labels_show'),
    path('create/', LabelViewCreate.as_view(), name='label_create'),
    path('<int:pk>/update/', LabelViewUpdate.as_view(), name='label_update'),
    path('<int:pk>/delete/', LabelViewDelete.as_view(), name='label_delete'),
]
