import pytest
from django.utils import timezone
from task.models import Tag, Task


@pytest.mark.django_db
def test_tag_creation():
    # Checks that a tag is created with the specified name and displays correctly
    tag = Tag.objects.create(name="Urgent")
    assert tag.name == "Urgent"
    assert str(tag) == "Urgent"


@pytest.mark.django_db
def test_unique_tag_name():
    # Checks that two tags with the same name cannot be created (unique constraint)
    Tag.objects.create(name="Work")
    with pytest.raises(Exception):
        Tag.objects.create(name="Work")


@pytest.mark.django_db
def test_task_creation():
    # Checks task creation with specific content and status
    task = Task.objects.create(
        content="Finish the project", date_of_creation=timezone.now(), done=False
    )
    assert task.content == "Finish the project"
    assert not task.done


@pytest.mark.django_db
def test_task_default_status():
    # Checks that a task has a default status of done=False
    task = Task.objects.create(
        content="New Task",
        date_of_creation=timezone.now(),
        done=False,  # Set done explicitly
    )
    assert not task.done


@pytest.mark.django_db
def test_task_tags_relationship():
    # Verifies the Many-to-Many relationship between tasks and tags
    tag1 = Tag.objects.create(name="Work")
    tag2 = Tag.objects.create(name="Personal")
    task = Task.objects.create(
        content="Read a book", date_of_creation=timezone.now(), done=False
    )
    task.tags.add(tag1, tag2)
    assert task.tags.count() == 2
    assert tag1 in task.tags.all()
    assert tag2 in task.tags.all()


@pytest.mark.django_db
def test_remove_tag_from_task():
    # Checks that a tag can be removed from a task
    tag = Tag.objects.create(name="Optional")
    task = Task.objects.create(
        content="Exercise", date_of_creation=timezone.now(), done=False
    )
    task.tags.add(tag)
    assert tag in task.tags.all()
    task.tags.remove(tag)
    assert tag not in task.tags.all()


@pytest.mark.django_db
def test_task_ordering():
    # Checks that tasks are ordered by creation date
    task1 = Task.objects.create(
        content="Task 1", date_of_creation=timezone.now(), done=False
    )
    task2 = Task.objects.create(
        content="Task 2",
        date_of_creation=timezone.now() + timezone.timedelta(minutes=5),
        done=False,
    )
    tasks = Task.objects.all()
    assert tasks[0] == task1
    assert tasks[1] == task2
