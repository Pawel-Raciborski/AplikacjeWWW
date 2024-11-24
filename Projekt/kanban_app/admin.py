from django.contrib import admin
from kanban_app.models import Board
from kanban_app.models import Column
from kanban_app.models import Task
from kanban_app.models import Comment


# Register your models here.
class BoardAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "description",
        "owner"
    ]
    list_filter = ['created_at']


class ColumnAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "board",
        "order",
    ]
    list_filter = ['created_at']


class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "description",
        "column",
        "priority",
        "due_date"
    ]
    list_filter = ['due_date']


class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "task",
        "user",
        "content",
    ]


admin.site.register(Board, BoardAdmin)
admin.site.register(Column, ColumnAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Comment, CommentAdmin)
