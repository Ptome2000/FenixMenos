import logging

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

from Vitae.models import Aluno, Curso, Sugestao, EstadoSub
from FenixMenos import settings
from serializers import UserAlunoSerializer, UserSerializer, CursoSerializer
import json


@api_view(['POST'])  # (2)
def RegistoAluno(request):
    user_serializer = UserSerializer(data=request.data)
    if user_serializer.is_valid():
        user = user_serializer.save()
        curso_codigo = request.data.get('curso')
        curso = Curso.objects.get(designacao=curso_codigo)
        foto = request.FILES.get('foto')
        aluno = Aluno(user=user, curso=curso, foto=foto)
        aluno.save()

        aluno_serializer = UserAlunoSerializer(aluno)
        return Response(aluno_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


def sugestoes(request):
    if request.method == 'POST' and 'action' in request.POST:
        action = request.POST['action']
        if action == 'Criar':
            assunto = request.POST['topic']
            mensagem = request.POST['message']
            Sugestao.objects.create(assunto=assunto, descricao=mensagem, user=request.user)
            messages.success(request, 'Sugestão criada com sucesso')
        elif action == 'Atualizar':
            id = request.POST['id']
            estado = request.POST['estado']
            s = Sugestao.objects.get(id=id)
            s.admin = request.user
            s.estado = int(estado)
            s.save()
            messages.success(request, 'Sugestão avaliada com sucesso')
    if request.user.is_superuser:
        sugs = Sugestao.objects.all()
        estados = EstadoSub.items()
        context = {'sugestoes': sugs, 'estados': estados}
    else:
        sugs = Sugestao.objects.filter(user=request.user)
        context = {'sugestoes': sugs}
    return render(request, 'sugestoes.html', context)