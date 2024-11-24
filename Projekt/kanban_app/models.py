from django.db import models
from rest_framework.authtoken.admin import User


# Create your models here.

class Board(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)
    users = models.ManyToManyField(User, related_name='boards')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Column(models.Model):
    name = models.CharField(max_length=256)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='columns')
    order = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class Priority(models.TextChoices):
    NISKI = "niski", "NISKI"
    SREDNI = "sredni", "SREDNI"
    WYSOKI = "wysoki", "WYSOKI"


class Task(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)
    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name='tasks')
    assign_users = models.ManyToManyField(User, related_name='tasks', blank=True)
    priority = models.CharField(choices=Priority.choices, max_length=16, default=Priority.NISKI)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(blank=True, null=True)


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)