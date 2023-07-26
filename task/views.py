from django.shortcuts import render

from task.models import Tag, Task


def index(request):
    num_tags = Tag.objects.count()
    num_tasks = Task.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_newspapers": num_tags,
        "num_redactors": num_tasks,
        "num_visits": num_visits + 1,
    }

    return render(request, "task/index.html", context=context)
