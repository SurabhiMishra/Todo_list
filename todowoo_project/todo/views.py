from django.db import IntegrityError
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from .forms import todoform
from .models import todo

# Create your views here.

def home(request):
    return render(request, 'todo/home.html')

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form': AuthenticationForm(),'error':'Username and password did not match' })
        else:
            login(request,user)
            return redirect('currenttodo')
        
       



def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currenttodo')

            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form': UserCreationForm(),'error':'Username already taken. Enter new username'})


             
        else:
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(),'error':'Passwrds did not match'})

def logoutuser(request):
    if request.method=='POST':
        pass
        logout(request)
        return redirect ('home')
           
def currenttodo(request):
    todos = todo.objects.filter(user=request.user)
    return render(request, 'todo/currenttodos.html',{'todos':todos})

def viewtodo(request,todo_pk):
    todox = get_object_or_404(todo,pk=todo_pk)
    form = todoform(instance=todox)
    return render(request, 'todo/viewtodo.html',{'todo':todox,'form':form})


def createtodo(request):
    if request.method=='GET':
        return render(request, 'todo/createtodo.html', {'form': todoform()})
    else:
        try:

            form = todoform(request.POST)
            newtodo=form.save(commit=False)
            newtodo.user=request.user
            newtodo.save()
            return redirect('currenttodo')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': todoform(),'error':'There is bad data'})



        
    
    


        
            
        

        
    


