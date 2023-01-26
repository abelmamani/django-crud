from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import crateTaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here

def home(request):
    #return HttpResponse('<h1> Hello world </h1>')
    return render(request, 'home.html')

def signup(request):
    if (request.method == 'GET'):
        return render(request, 'signup.html', {
        'form': UserCreationForm })
    else: 
        if(request.POST['password1'] == request.POST['password2']):
            try:
                user = User.objects.create_user(username = request.POST['username'], password = request.POST['password1'])
                user.save()
                login(request, user)
                #return HttpResponse('USUARUIO CREATED SUCCESSFULY')
                return redirect('tasks')
            except IntegrityError:
                 return render(request, 'signup.html', { 'form': UserCreationForm, 'error': 'username already exists'}) 
        else:
            return render(request, 'signup.html', { 'form': UserCreationForm, 'error': 'password do not match'}) 

@login_required
def tasks(request):
    tasks  = Task.objects.filter(user = request.user, datecompleted__isnull = True)
    return render(request, 'tasks.html', {'tasks': tasks})


@login_required
def tasks_completed(request):
    tasks  = Task.objects.filter(user = request.user, datecompleted__isnull = False).order_by('-datecompleted')
    return render(request, 'tasks.html', {'tasks': tasks})


@login_required
def task_detail(request, task_id):
    if(request.method == 'GET'):
        task = get_object_or_404(Task, pk = task_id, user = request.user)
        form = crateTaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else: 
        try: 
            task = get_object_or_404(Task, pk = task_id, user = request.user)
            form = crateTaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError: 
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': 'erorr en los datos'})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk = task_id, user = request.user)
    if(request.method == 'POST'):
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk = task_id, user = request.user)
    if(request.method == 'POST'):
        task.delete()
        return redirect('tasks')

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
        'form': crateTaskForm
        })
    else: 
        try:
            form = crateTaskForm(request.POST)
            newTask = form.save(commit=False)
            newTask.user = request.user
            newTask.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
            'form': crateTaskForm,
            'error': 'por favor dale datos validos'
            })



@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
        'form': AuthenticationForm })
    else:
        #int(request.POST)
        
        u = request.POST.get('username')
        p = request.POST.get('password')
      
        user = authenticate(request, username=u, password=p)
        #print(User.objects.get(username = u).email)
        #print(user)
      
        if user is None:
              return render(request, 'signin.html', { 'form': AuthenticationForm, 'error': 'username or password is incorrect'})
        else:
            login(request, user)
            return redirect('tasks')

def prueba(request):
    return HttpResponse('Prueba')
      

    


