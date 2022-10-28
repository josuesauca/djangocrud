"""crud URL Configuration

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
from unicodedata import name
from django.contrib import admin
from django.urls import path
from task import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("vista/",views.helloWorld),
    path("signup/",views.SignUp),
    path("tasks/",views.Tasks, name = "tasks"),
    path("taskscompleted/",views.TasksCompleted, name = "taskscompleted"),
    path("",views.Base, name = "base"),
    path("logout/",views.LogOut, name = "logout"),
    path("signin/",views.SignIn, name = "signin"),
    path("createtask/",views.CreateTask, name = "createtask"),
    path("taskdetail/<int:task_id>",views.TaskDetail, name = "taskdetail"),
    path("taskdetail/<int:task_id>/complete",views.CompleteTask, name = "completetask"),
    path("taskdetail/<int:task_id>/delete",views.DeleteTask, name = "deletetask"),
    path("home/",views.Home, name = "home")

]
