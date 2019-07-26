from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render


def Hello(request):
    print("hahaha")
    return HttpResponse("hello")


def Heihei(request):
    print("hahaha")
    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'html/create.html', context)