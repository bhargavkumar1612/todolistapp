from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .models import todo
from .forms import TodoForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required 

# Create your views here.
def home(request):
	return render(request, 'todoapp/home.html')

def signinuser(request):
	try:
		if request.user.is_authenticated:
			return redirect('home')
	except:
		pass
	if request.method == 'GET':
		return render(request, 'todoapp/signinuser.html', {'form':AuthenticationForm()})
	else:
		user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
		if user is None:
			return render(request, 'todoapp/signinuser.html', {'form':AuthenticationForm(),'error':'credintials didnot match'})

		else:
			login(request, user)
			return redirect('currenttodos')



def signupuser(request):
	if request.method == 'GET':
		return render(request, 'todoapp/signupuser.html', {'form':UserCreationForm()})
	else:
		if request.POST['password1']== request.POST['password2']:
			try:
				user = User.objects.create_user(username = request.POST['username'], password = request.POST['password1'])
				user.save()
				login(request, user)
				return redirect('currenttodos')
			except IntegrityError:
				return render(request, 'todoapp/signupuser.html', {'form':UserCreationForm(), 'error':'username already taken.'})
		else:
			return render(request, 'todoapp/signupuser.html', {'form':UserCreationForm(), 'error':'passwords didnot match'})


@login_required
def logoutuser(request):
	if request.method == 'POST':
		logout(request)
		return redirect('home')


@login_required
def currenttodos(request):
	if request.user.is_authenticated:
		todos = todo.objects.filter(user = request.user, datecompleted__isnull=True).order_by('-created')
		completedTodos = todo.objects.filter(user = request.user, datecompleted__isnull=False).order_by('-datecompleted')
		return render(request, 'todoapp/currenttodos.html', {'todos':todos, 'completed':completedTodos})
	else:
		return redirect('home')


@login_required
def createtodo(request):
	if request.method == 'GET':
		return render(request, 'todoapp/createtodo.html', {'form':TodoForm()})
	else:
		try:
			form  = TodoForm(request.POST)
			newtodo = form.save(commit=False)
			newtodo.user = request.user
			newtodo.save()
			return redirect('currenttodos')
		except ValueError:
			return render(request, 'todoapp/createtodo.html', {'form':TodoForm(), 'error':'Data incompatible try again'})

@login_required
def viewtodo(request, todo_pk):
	todd = get_object_or_404(todo, pk=todo_pk, user = request.user )
	completed = todd.datecompleted != None
	if request.method == 'GET':
		form = TodoForm(instance = todd)
		return render(request, "todoapp/viewtodo.html", {'todo':todd,'form':form, 'completed':completed})
	elif request.method == 'POST':
		try:
			form  = TodoForm(request.POST, instance = todd)
			form.save()
			return redirect('currenttodos')
		except ValueError:
			return render(request, 'todoapp/viewtodo.html', {'form':TodoForm(instance = todd), 'error':'Data incompatible try again'})

@login_required
def edittodo(request, todo_pk):
	todd = get_object_or_404(todo, pk=todo_pk, user = request.user )
	completed = todd.datecompleted != None
	if request.method == 'GET':
		form = TodoForm(instance = todd)
		return render(request, "todoapp/edittodo.html", {'todo':todd,'form':form, 'completed':completed})
	elif request.method == 'POST':
		try:
			form  = TodoForm(request.POST)
			newtodo = form.save(commit=False)
			newtodo.user = request.user
			newtodo.save()
			todd.delete()
			return redirect('currenttodos')
		except ValueError:
			return render(request, 'todoapp/edittodo.html', {'form':TodoForm(instance = todd), 'error':'Data incompatible try again'})


@login_required
def completetodo(request, todo_pk):
	todd = get_object_or_404(todo, pk=todo_pk, user = request.user)
	if request.method == 'POST':
		todd.datecompleted = timezone.now()
		todd.save()
		return redirect('currenttodos')


@login_required
def deletetodo(request, todo_pk):
	todd = get_object_or_404(todo, pk=todo_pk, user = request.user)
	if request.method == 'POST':
		todd.delete()
		return redirect('currenttodos')


@login_required
def readdtodo(request, todo_pk):
	todd = get_object_or_404(todo, pk=todo_pk, user = request.user)
	if request.method == 'POST':
		form = TodoForm(instance = todd)
		todd.delete()
		newtodo = form.save(commit=False)
		newtodo.datecompleted = None
		newtodo.user = request.user
		newtodo.save()
		return redirect('currenttodos')
