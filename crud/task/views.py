from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.contrib.auth.decorators import login_required



def helloWorld(request):
    return render(request, "SignUp.html", {"form": UserCreationForm})


def Home(request):
    return render(request, "Home.html")


def Base(request):
    return render(request, "Base.html")


@csrf_exempt
def SignUp(request):
    if request.method == "GET":
        return render(request, "SignUp.html", {"form": UserCreationForm})
    else:
        try:
            if request.POST["password1"] == request.POST["password2"]:
                user = User.objects.create_user(
                    username=request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect("tasks")
        except IntegrityError:
            return render(request, "SignUp.html", {"form": UserCreationForm,
                                                   "error": "Username already exists"})
    return render(request, "SignUp.html", {"form": UserCreationForm,
                                           "error": "Password do not match"})

@login_required
def Tasks(request):
    tasks = Task.objects.filter(user=request.user, dateCompleted__isnull=True)
    return render(request, "Tasks.html", {"tasks": tasks})

@login_required
def TasksCompleted(request):
    tasks = Task.objects.filter(user=request.user, dateCompleted__isnull=False).order_by('-dateCompleted')
    return render(request, "Tasks.html", {"tasks": tasks})


def LogOut(request):
    logout(request)
    return redirect("home")


def SignIn(request):
    if request.method == "GET":
        return render(request, "SignIn.html", {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST["username"], password=request.POST["password"])
        print(user, "4545")

        if user is None:
            print("No entra")
            return render(request, "SignIn.html", {"form": AuthenticationForm, "error": "Username or password is incorrect"})
        else:
            print("Entra")
            login(request, user)
            return redirect("tasks")

@login_required
def CreateTask(request):
    if request.method == "GET":
        return render(request, "Create_Task.html", {"form": TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            if form.is_valid():
                newTask = form.save(commit=False)
                if newTask.is_valid():
                    newTask.user = request.user
                    newTask.save()
                    return redirect("tasks")
        except:
            return render(request, "Create_Task.html", {"form": TaskForm, "error": "Por favor valide los datos"})

@login_required
def TaskDetail(request, task_id):

    task = get_object_or_404(Task, pk=task_id, user = request.user)

    if request.method == "GET":
        #task = Task.objects.get(pk=task_id)
        form = TaskForm(instance=task)
        return render(request, "TaskDetail.html", {"task": task, "form": form})
    else:
        try:
            #jtask = get_object_or_404(Task, pk=task_id, user = request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            if form.is_valid():
                return redirect("tasks")
        except ValueError:
            return render(request, "TaskDetail.html", {"task": task, "form": form, "error":"Error updating task"})

        # return render(request, "TaskDetail.html",{"task":task,"form":form})
@login_required
def CompleteTask(request,task_id):
    task = get_object_or_404(Task,pk = task_id,user = request.user)
    if(request.method == "POST"):
        task.dateCompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def DeleteTask(request,task_id):
    task = get_object_or_404(Task,pk = task_id,user = request.user)
    if(request.method == "POST"):
        task.delete()        
        return redirect('tasks')



