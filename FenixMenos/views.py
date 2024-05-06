from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.timezone import now

from Vitae.models import Aluno
from FenixMenos import settings


def index(request):
    return render(request, 'index.html')


def loginform(request):
    if request.method == 'POST':
        username = request.POST['username']
        passwd = request.POST['password']
        user = authenticate(username=username, password=passwd)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.warning(request, 'Username ou Password incorretos')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def logoutForm(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def registro(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        #curso = request.POST['curso']
        #comentario = request.POST['comentario']
        if password == request.POST['passwordConfirm']:
            u = User.objects.create_user(username, email, password, last_login=now())
           #a = Aluno(user=u)
           #a.save()
            messages.success(request, 'Conta criada com sucesso, por favor faça login com as suas credenciais')
            return HttpResponseRedirect(reverse('login'))
        else:
            messages.warning(request, 'Passwords não coincidem')
            return render(request, 'registar.html')
    else:
        return render(request, 'registar.html')
