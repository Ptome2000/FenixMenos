from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from Vitae.models import Aluno, Curso
from FenixMenos import settings
from serializers import UserAlunoSerializer, UserSerializer
import json


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])  # (2)
def RegistoAluno(request):
    if request.method == 'GET':  # (3)
        CursoSerializer = Curso.objects.all()
        serializer = UserAlunoSerializer(CursoSerializer, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':  # (3)
        serializer = UserAlunoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


def registo(request):
    cursos = Curso.objects.all()  # Recupera todos os cursos para o dropdown
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        curso_codigo = request.POST['curso']

        if password == request.POST['passwordConfirm']:
            user = User.objects.create_user(username, email, password, last_login=now())
            foto = request.FILES.get('foto', None)
            curso = Curso.objects.get(codigo=curso_codigo)
            aluno = Aluno(user=user, curso=curso, foto=foto)
            aluno.save()

            messages.success(request, 'Conta criada com sucesso, por favor faça login com as suas credenciais')
            return HttpResponseRedirect(reverse('login'))  # Redireciona para a página de login após registro
        else:
            messages.warning(request, 'Passwords não coincidem')
            return render(request, 'registar.html', {'cursos': cursos})
    else:
        return render(request, 'registar.html', {'cursos': cursos})
