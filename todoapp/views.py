from django . shortcuts import render, redirect
from django.contrib.auth.models import User
from todoapp import models
from todoapp.models import TODO
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        emailid = request.POST.get('email')
        pwd = request.POST.get('pwd')
        print(fnm, emailid, pwd)
        my_user = User.objects.create_user(fnm, emailid, pwd)
        my_user.save()
        return redirect('/login')
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        pwd = request.POST.get('pwd')
        print(fnm, pwd)
        user = authenticate(request, username=fnm, password=pwd)
        if user is not None:
            login(request, user)  # tetap panggil login di sini
            return redirect('todoapp')
        else:
            return redirect('login')
    return render(request, 'login.html')

@login_required(login_url='/login/')
def todoapp(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        print(title)
        obj = models.TODO(title=title, user=request.user)
        obj.save()
        res = models.TODO.objects.filter(user = request.user).order_by('-date')
        return redirect('/todoapp', {'res': res})
    res = models.TODO.objects.filter(user = request.user).order_by('-date')    
    return render(request, 'todoapp.html', {'res': res})

@login_required(login_url='/login/')
def edit_todo(request, srno):
    obj = models.TODO.objects.get(srno=srno, user=request.user)  # Pastikan hanya milik user
    if request.method == 'POST':
        title = request.POST.get('title')
        obj.title = title
        obj.save()
        return redirect('todoapp')  # Redirect ke halaman utama tanpa parameter
    return render(request, 'edit_todo.html', {'obj': obj})  # Render template edit_todo.html


@login_required(login_url='/login/')
def delete_todo(request, srno):
    obj = models.TODO.objects.get(srno = srno)
    obj.delete()
    return redirect('/todoapp')

def signout(request):
    logout(request)
    return redirect('/login')