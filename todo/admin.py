from django.contrib import admin
from .models import Todolist, Comment, Projectlist


class TodolistAdmin(admin.ModelAdmin):
    readonly_fields = ('date_created',)
    search_fields = ['title', 'memo']


admin.site.register(Todolist, TodolistAdmin)
admin.site.register(Comment)
admin.site.register(Projectlist)
