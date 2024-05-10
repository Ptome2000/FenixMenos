from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from .models import *


def perfil(request):
    user = request.user
    context = {'user': user}
    return render(request, 'Vitae/perfil.html', context)



def detalhes_curso(request, codigo):
    curso = get_object_or_404(Curso, codigo=codigo)
    planos_curriculares = PlanoCurricular.objects.filter(curso=curso)
    context = {'curso': curso, 'planos_curriculares': planos_curriculares}
    return render(request, 'Vitae/detalhes_curso.html', context)


def detalhes_uc(request, acronimo):
    uc = get_object_or_404(UC, acronimo=acronimo)
    planos_curriculares = PlanoCurricular.objects.filter(uc=uc)
    equipa = EquipaDocente.objects.filter(uc=uc)

    context = {'uc': uc, 'planos_curriculares': planos_curriculares, 'equipa': equipa}
    return render(request, 'Vitae/detalhes_uc.html', context)


# Adicionar validaão que tem que ser prof
def UnidadesCurriculares(request):
        unidades = EquipaDocente.objects.filter(professor=request.user.professor)

        context = {'unidades': unidades}
        return render(request, 'Vitae/listar_prof_uc.html', context)



def fazer_upload(request):
    user = request.user
    if request.method == 'POST' and request.FILES.get('myfile') is not None:
        myfile = request.FILES['myfile']
        if hasattr(user, 'aluno'):
            aluno = Aluno.objects.get(user=request.user)
            aluno.avatar = myfile
            aluno.save()
        elif hasattr(user, 'professor'):
            professor = Professor.objects.get(user=request.user)
            professor.avatar = myfile
            professor.save()
        messages.success(request, "A sua foto foi carregada com sucesso!")
        return redirect(reverse('Vitae:perfil'))
    else:
        messages.error(request, "Erro ao fazer o upload.")
        return redirect(reverse('Vitae:perfil'))



