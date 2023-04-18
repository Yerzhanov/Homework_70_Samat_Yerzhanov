"""To_do_list URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from todo.views import *
from issue_tracker.views import CommentListView, CommentDetailView, CommentCreateView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('todo', TodoViewSet)

project = routers.DefaultRouter()
project.register('projects', ProjectViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('list/', CommentListView.as_view(), name='list'),
    path('tickets/<int:tickets_pk>/', CommentDetailView.as_view(), name='detail_view'),
    path('add/', CommentCreateView.as_view(), name='add'),

    path('signup/', signupuser, name='signupuser'),
    path('login/', loginuser, name='loginuser'),
    path('logout/', logoutuser, name='logoutuser'),
    path('create_user/', RegisterView.as_view(), name='create_user'),

    path('', HomeView.as_view(), name='home'),
    path('current/', CurrentView.as_view(), name='currenttodos'),
    path('create/', createtodo, name='createtodo'),
    path('createcomment/', createcomment, name='createcomment'),
    path('completed/', CompleteTodosView.as_view(), name='completedtodos'),

    path('todo/<int:todo_pk>', viewtodo, name='viewtodo'),
    path('view_comments/', viewcomment, name='viewcomment'),
    path('todo/<int:todo_pk>/complete', completetodo, name='completetodo'),
    path('todo/<int:todo_pk>/delete', deletetodo, name='deletetodo'),

    path('list_project/', ProjectView.as_view(), name='list_project'),
    path('create_project/', ProjectCreateView.as_view(), name='create_project'),
    path('view_project/<slug:pk>/', ProjectDetailView.as_view(), name='view_project'),

    path('', include(router.urls)),
    path('', include(project.urls)),

]


