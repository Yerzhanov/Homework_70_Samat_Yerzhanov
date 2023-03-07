from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm, CommentForm
from .models import Todolist, Comment
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView


class HomeView(TemplateView):
    template_name = 'todo/home.html'
    extra_context = {'title': 'Домашняя страница'}


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'Такой пользователь уже существует. Задайте новое имя.'})
        else:
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'Пароль не совпадает'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form': AuthenticationForm(), 'error': 'Пользователь и пароль не найдены'})
        else:
            login(request, user)
            return redirect('currenttodos')

@login_required()
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required()
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            new_to_do = form.save(commit=False)
            new_to_do.user = request.user
            new_to_do.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': TodoForm(), 'error': 'Были переданы неверные данные. Попробуйте снова.'})

@login_required()
def createcomment(request):
    if request.method == 'GET':
        return render(request, 'todo/create_comment.html', {'form': CommentForm()})
    else:
        try:
            form = CommentForm(request.POST)
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/create_comment.html', {'form': CommentForm(), 'error': 'Были переданы неверные данные. Попробуйте снова.'})

@login_required()
def viewcomment(request):
    comments = Comment.objects.all()
    return render(request, 'todo/view_comment.html', {'comments': comments})


class CurrentView(ListView):
    model = Todolist
    template_name = 'todo/currenttodos.html'
    extra_context = {'title': 'Общий список дел'}

    def get_context_data(self, **kwargs):
       context = super(CurrentView, self).get_context_data()
       context['todos'] = Todolist.objects.all()
       return context


class CompleteTodosView(ListView):
    model = Todolist
    template_name = 'todo/completedtodos.html'
    extra_context = {'title': 'Список выполненных дел'}

    def get_context_data(self, **kwargs):
       context = super(CompleteTodosView, self).get_context_data()
       context['todos'] = Todolist.objects.filter(date_completed__isnull=False)
       return context


@login_required()
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todolist, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.date_completed = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required()
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todolist, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')

@login_required()
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todolist, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form, 'error': 'Неправильно введеные данные'})