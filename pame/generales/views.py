from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Create your views here.



def home(request):
    return render(request,'home.html')

def menu(request):
    return render(request, 'menu.html')


def exit(request):
    logout(request)
    return redirect('home')