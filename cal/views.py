from django.shortcuts import render, reverse, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='cal:login')
def home(request):
    return render(request, 'index.html', {})


def login(request):
    return render(request, 'login.html', {})


def logout(request):
    auth_logout(request)
    return redirect(reverse('login'))
