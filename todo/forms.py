from django.forms import ModelForm
from .models import Todolist, Comment


class TodoForm(ModelForm):
    class Meta:
        model = Todolist
        fields = ['title', 'memo', 'important']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['article', 'text', 'author', 'status', 'task_type', 'tags']