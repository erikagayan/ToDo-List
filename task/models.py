from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class Task(models.Model):
    content = models.TextField()
    date_of_creation = models.DateField()
    done = models.BooleanField()
    tags = models.ManyToManyField(Tag, related_name="tasks")
