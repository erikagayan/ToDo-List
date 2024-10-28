import pytest
from django.urls import reverse, resolve
from task.views import (
    TaskListView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TagListView,
    TagCreateView,
    TagUpdateView,
    TagDeleteView,
    change_status,
)


@pytest.mark.parametrize(
    "url_name, view",
    [
        ("task:task-list", TaskListView),
        ("task:task-create", TaskCreateView),
        ("task:task-update", TaskUpdateView),
        ("task:task-delete", TaskDeleteView),
        ("task:tag-list", TagListView),
        ("task:tag-create", TagCreateView),
        ("task:tag-update", TagUpdateView),
        ("task:tag-delete", TagDeleteView),
        ("task:change_status", change_status),
    ],
)
def test_url_resolves_to_correct_view(url_name, view):
    if "update" in url_name or "delete" in url_name or url_name == "task:change_status":
        url = reverse(url_name, args=[1])
    else:
        url = reverse(url_name)
    assert (
        resolve(url).func.view_class == view
        if isinstance(view, type)
        else resolve(url).func == view
    )
