from django.shortcuts import render

from FenixMenos import settings


def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')
