from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User

from lists.forms import TodoForm
from lists.models import Todo

# READ
@login_required
def index(request):
    user = request.user if request.user.is_authenticated else None
    userAccount = User.objects.get(username=user)
    todolist = Todo.objects.filter(creator_id = userAccount)

    if request.method == "POST":
        return redirect("lists:add_todo")

    return render(request, "lists/todolist.html", {"todolist": todolist, "form": TodoForm()})


# TO DO LIST
def todolist(request):
    user = request.user if request.user.is_authenticated else None
    userAccount = User.objects.filter(username=user)
    todolist = Todo.objects.filter(creator_id = userAccount)
    if request.method == "POST":
        redirect("lists:add_todo")

    return render(
        request, "lists/todolist.html", {"todolist": todolist, "form": TodoForm()}
    )

# CREATE
def add_todo(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            user = request.user if request.user.is_authenticated else None
            todo = Todo(
                description=request.POST["description"],
                creator=user,
            )
            todo.save()
            return redirect("lists:index")
        else:
            return render(request, "lists/todolist.html", {"form": form})

    return redirect("lists:index")



