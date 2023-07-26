from django.shortcuts import render
from django.views import generic

from task.models import Tag, Task


class TaskListView(generic.ListView):
    model = Task
