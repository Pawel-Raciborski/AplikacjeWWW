from rest_framework import serializers
from .models import Board
from .models import Column
from .models import Task
from .models import Comment


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = ['id', 'created_at']


class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = "__all__"
        read_only_fields = ['id', 'created_at']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ['id', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ['id', 'created_at']
