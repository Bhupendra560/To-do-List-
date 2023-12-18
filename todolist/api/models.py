from django.db import models
from django.utils import timezone
from todolist.settings import STATUS_CHOICES

class Task(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=1000)
    due_date = models.DateField(blank=True, null=True)
    tags = models.ManyToManyField('Tag', blank=True) 
    timestamp = models.DateTimeField(default=timezone.now, editable=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OPEN')

    class Meta:
        db_table="tbltask"

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table="tbltag"


