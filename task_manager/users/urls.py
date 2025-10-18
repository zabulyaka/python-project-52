from django.urls import path

# from task_manager.users import views
from task_manager.users.views import (
    UsersView,
    UserViewCreate,
    UserViewDelete,
    UserViewUpdate,
)

urlpatterns = [
#    path('', views.index),
    path('', UsersView.as_view(), name='users_show'),
    path('create/', UserViewCreate.as_view(), name='user_create'),
    path('<int:id>/update/', UserViewUpdate.as_view(), name='user_update'),
    path('<int:id>/delete/', UserViewDelete.as_view(), name='user_delete'),
]
