from django.shortcuts import render

from FenixMenos import settings


def index(request):
    return render(request, 'index.html', {'MEDIA_URL': settings.MEDIA_URL})


def login(request):
    return render(request, 'login.html')
