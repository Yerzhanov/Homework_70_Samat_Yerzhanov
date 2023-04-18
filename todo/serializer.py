from rest_framework import serializers
from .models import Todolist, Projectlist


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todolist
        fields = ['id', 'title', 'memo', 'user', 'status', 'project', 'date_created']




