from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Todo
from .forms import TodoForm, UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate, login as auth_login


# Create your views here.


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            login(request, user)  # Log the user in after registration
            return redirect('list_todos')  # Redirect to the TODO list page after signup
    else:
        form = UserCreationForm()  # Show the signup form if GET request
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)  # Log the user in
                return redirect('list_todos')  # Redirect to the TODO list page after login
    else:
        form = AuthenticationForm()  # Show the login form if GET request
    return render(request, 'registration/login.html', {'form': form})

def custom_logout(request):
    logout(request)  # Logout the user
    return redirect('/')  # Redirect to the homepage or any other page

@login_required
def list_todos(request):
    todos = Todo.objects.filter(user=request.user)
    return render(request, 'todo/list_doto.html', {'todos': todos})

@login_required
def create_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect('list_todos')
    else:
        form = TodoForm()
    return render(request, 'todo/create_todo.html', {'form': form})

@login_required
def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    todo.delete()
    return redirect('list_todos')
