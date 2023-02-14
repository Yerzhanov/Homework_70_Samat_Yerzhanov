from django.forms import ModelForm
from .models import Todolist


class TodoForm(ModelForm):
    class Meta:
        model = Todolist
        fields = ['title', 'memo', 'important']