from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    date_of_creation = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
        label="Date of creation*",
    )

    class Meta:
        model = Task
        fields = "__all__"
