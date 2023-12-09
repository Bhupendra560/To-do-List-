from django.db import models
from django.utils import timezone
from todolist.settings import STATUS_CHOICES

class Task(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    due_date = models.DateTimeField(blank=True, null=True)
    tags = models.ManyToManyField('Tag', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OPEN')

    def __str__(self):
        return self.title
    class Meta:
        db_table="tbltask"

class Tag(models.Model):
    value = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.value

