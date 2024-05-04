from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from Vitae.models import Aluno

def is_professor(user):
    return hasattr(user, 'professor')

def is_aluno(user):
    return hasattr(user, 'aluno')

def perfil(request):
    # Aqui você pode adicionar lógica para buscar dados do usuário ou suas Skills
    return render(request, 'perfil.html')

def fazer_upload(request):
    if request.method == 'POST' and request.FILES.get('myfile') is not None:
        myfile = request.FILES['myfile']
        a = Aluno.objects.get(user=request.user)
        a.avatar = myfile
        a.save()
        messages.success(request, "A sua foto foi carregada com sucesso")
    return HttpResponseRedirect(reverse('Vitae:perfil'))