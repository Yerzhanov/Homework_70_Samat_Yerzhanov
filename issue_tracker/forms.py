from django import forms
from .models import Ticket
from django.core.validators import MinLengthValidator

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'text', 'author', 'status', 'task_type']