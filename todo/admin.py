from django.contrib import admin
from .models import Todolist


class TodolistAdmin(admin.ModelAdmin):
    readonly_fields = ('date_created',)


admin.site.register(Todolist, TodolistAdmin)



