from django import forms
from .models import Todolist, Comment
from django.core.validators import MinLengthValidator


class TodoForm(forms.ModelForm):
    title = forms.CharField(max_length=100, validators=(MinLengthValidator(limit_value=5, message="Заголовок должен быть больше 5 символов"),))
    class Meta:
        model = Todolist
        fields = ['title', 'memo', 'important', 'status']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['article', 'text', 'author', 'status', 'task_type', 'tags']

