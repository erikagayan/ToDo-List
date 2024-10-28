import pytest
from django.utils import timezone
from task.forms import TaskForm
from task.models import Tag


@pytest.mark.django_db
def test_task_form_valid_data():
    # Checks that the form is valid with correct data
    tag = Tag.objects.create(name="Work")
    form_data = {
        "content": "Test task",
        "date_of_creation": timezone.now().strftime("%Y-%m-%dT%H:%M"),
        "done": False,
        "tags": [tag.id],
    }
    form = TaskForm(data=form_data)

    # Output form errors if validation fails
    if not form.is_valid():
        print("Form errors:", form.errors)

    assert form.is_valid()  # Validating form without tags

    task = form.save(commit=False)
    task.save()
    task.tags.add(tag)  # Add tags separately after saving

    assert task.tags.count() == 1
    assert tag in task.tags.all()


@pytest.mark.django_db
def test_task_form_invalid_data():
    # Checks that the form is invalid when a required field is missing
    form_data = {
        "date_of_creation": timezone.now(),
        "done": False,
    }
    form = TaskForm(data=form_data)
    assert not form.is_valid()
    assert "content" in form.errors


@pytest.mark.django_db
def test_task_form_date_widget():
    # Checks that the date_of_creation field uses a widget of type datetime-local
    form = TaskForm()
    widget_type = form.fields["date_of_creation"].widget.input_type
    assert widget_type == "datetime-local"
