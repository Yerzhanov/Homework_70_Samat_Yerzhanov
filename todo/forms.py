from django import forms
from .models import Todolist, Comment, Projectlist


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todolist
        fields = ['title', 'memo', 'important', 'status', 'project']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Projectlist
        fields = ['name', 'description', 'date_created', 'date_completed']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['article', 'text', 'author', 'status', 'task_type', 'tags']


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Найти")

