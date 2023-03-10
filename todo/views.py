from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.utils.http import urlencode
from django.views.generic import CreateView, DetailView

from .forms import TodoForm, CommentForm, SimpleSearchForm, ProjectForm
from .models import Todolist, Comment, Projectlist
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

def deletecomment(request,article_pk):
    comments = get_object_or_404(Comment, pk=article_pk, user=request.user)
    if request.method == 'POST':
        comments.delete()
        return redirect('currenttodos')


class CurrentView(ListView):
    context_object_name = 'todos'
    model = Todolist
    template_name = 'todo/currenttodos.html'
    ordering = ['-date_created']
    paginate_by = 10
    paginate_orphans = 1
    extra_context = {'title': 'Общий список'}

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(memo__icontains=self.search_value) | Q(title__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None


class CompleteTodosView(ListView):
    model = Todolist
    template_name = 'todo/completedtodos.html'
    paginate_by = 10
    extra_context = {'title': 'Список выполненных дел'}

    def get_context_data(self, **kwargs):
       context = super(CompleteTodosView, self).get_context_data()
       context['todos'] = Todolist.objects.filter(date_completed__isnull=False).order_by('-date_completed')
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
        todo.date_deleted = timezone.now()
        todo.delete()
        return redirect('currenttodos')


class ProjectView(ListView):
    context_object_name = 'projects'
    model = Projectlist
    template_name = 'todo/list_project.html'
    ordering = ['-date_created']
    paginate_by = 3
    paginate_orphans = 1
    extra_context = {'title': 'Список проектов'}

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(name__icontains=self.search_value) | Q(description__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None

class ProjectDetailView(DetailView):
    template_name = 'todo/view_project.html'
    model = Projectlist

class ProjectCreateView(CreateView):
    template_name = 'todo/createproject.html'
    model = Projectlist
    form_class = ProjectForm

    def get_redirect_url(self):
        return reverse('list_project', kwargs={'pk': self.object.pk})

# class ProjectUpdateView(UpdateView):
#     model = Article
#     template_name = 'article/update.html'
#     form_class = ArticleForm
#     context_key = 'article'
#
#
#     def get_redirect_url(self):
#         return reverse('article_view', kwargs={'pk': self.object.pk})