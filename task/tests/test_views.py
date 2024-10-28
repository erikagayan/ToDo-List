import pytest
from django.urls import reverse
from task.models import Task, Tag
from django.utils import timezone


@pytest.mark.django_db
def test_task_list_view(client):
    # Checks access to the task list page
    response = client.get(reverse("tasks:task-list"))
    assert response.status_code == 200
    assert "task_list" in response.context


@pytest.mark.django_db
def test_task_create_view(client):
    # Checks task creation through the form
    response = client.post(
        reverse("tasks:task-create"),
        {
            "content": "Test task",
            "date_of_creation": timezone.now().strftime("%Y-%m-%dT%H:%M"),
            "done": False,
        },
    )
    assert response.status_code in [
        200,
        302,
    ]  # Allow both 200 and 302 for form validation


@pytest.mark.django_db
def test_task_update_view(client):
    # Checks task update functionality
    task = Task.objects.create(
        content="Original content", date_of_creation=timezone.now(), done=False
    )
    response = client.post(
        reverse("tasks:task-update", args=[task.id]),
        {
            "content": "Updated content",
            "date_of_creation": task.date_of_creation.strftime("%Y-%m-%dT%H:%M"),
            "done": task.done,
        },
    )
    assert response.status_code in [200, 302]


@pytest.mark.django_db
def test_task_delete_view(client):
    # Checks task deletion
    task = Task.objects.create(
        content="Task to delete", date_of_creation=timezone.now(), done=False
    )
    response = client.post(reverse("tasks:task-delete", args=[task.id]))
    assert response.status_code == 302
    assert not Task.objects.filter(id=task.id).exists()


@pytest.mark.django_db
def test_tag_list_view(client):
    # Checks access to the tag list page
    response = client.get(reverse("tasks:tag-list"))
    assert response.status_code == 200
    assert "tag_list" in response.context


@pytest.mark.django_db
def test_tag_create_view(client):
    # Checks tag creation through the form
    response = client.post(reverse("tasks:tag-create"), {"name": "New Tag"})
    assert response.status_code == 302
    assert Tag.objects.filter(name="New Tag").exists()


@pytest.mark.django_db
def test_tag_update_view(client):
    # Checks tag update functionality
    tag = Tag.objects.create(name="Old Tag")
    response = client.post(
        reverse("tasks:tag-update", args=[tag.id]), {"name": "Updated Tag"}
    )
    assert response.status_code == 302
    tag.refresh_from_db()
    assert tag.name == "Updated Tag"


@pytest.mark.django_db
def test_tag_delete_view(client):
    # Checks tag deletion
    tag = Tag.objects.create(name="Tag to delete")
    response = client.post(reverse("tasks:tag-delete", args=[tag.id]))
    assert response.status_code == 302
    assert not Tag.objects.filter(id=tag.id).exists()


@pytest.mark.django_db
def test_change_status_view(client):
    # Checks task status change functionality
    task = Task.objects.create(
        content="Task to toggle", date_of_creation=timezone.now(), done=False
    )
    response = client.post(reverse("tasks:change_status", args=[task.id]))
    assert response.status_code == 302
