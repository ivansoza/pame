from django.shortcuts import render

# Create your views here.


def homeComedor(request):
    return render (request,"homeComedor.html")

