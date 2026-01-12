from django.urls import path
from .views import (
    TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView,
    TagListView, TagCreateView, TagUpdateView, TagDeleteView,
    toggle_task_status
)

urlpatterns = [
    # Головна сторінка з завданнями
    path("", TaskListView.as_view(), name="index"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("tasks/<int:pk>/toggle/", toggle_task_status, name="toggle-status"),

    # Сторінка з тегами
    path("tags/", TagListView.as_view(), name="tag-list"),
    path("tags/create/", TagCreateView.as_view(), name="tag-create"),
    path("tags/<int:pk>/update/", TagUpdateView.as_view(), name="tag-update"),
    path("tags/<int:pk>/delete/", TagDeleteView.as_view(), name="tag-delete"),
]

app_name = "todo"