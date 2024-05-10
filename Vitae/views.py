
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from .models import *

def perfil(request):
    user = request.user
    context = {}
    if user.is_authenticated:
        if hasattr(user, 'aluno'):
            aluno = get_object_or_404(Aluno, user=user)
            aluno_skills = Skills.objects.filter(aluno=aluno)
            matriculas = Matricula.objects.filter(aluno=aluno).select_related('curso')
            notas = Nota.objects.filter(aluno=aluno).select_related('uc')
            uc_notas = {nota.uc.acronimo: nota.nota for nota in notas}
            recomendacoes = Recomendacao.objects.filter(aluno=aluno)
            curso = aluno.curso
            context = {
                'usuario': aluno,
                'skills': aluno_skills,
                'matriculas': matriculas,
                'notas': uc_notas,  # pass this dictionary to the template
                'recomendacoes': recomendacoes,
                'curso': curso,
            }
        elif hasattr(user, 'professor'):
            professor = get_object_or_404(Professor, user=user)
            ucs = UC.objects.filter(coordenador=professor)
            gabinete = professor.gabinete
            context = {
                'usuario': professor,
                'gabinete': gabinete,
                'ucs': ucs,
            }
    else:
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'perfil.html', context)


def detalhes_curso(request, codigo):
    curso = get_object_or_404(Curso, codigo=codigo)
    ucs = curso.uc_set.all()
    context = {'curso': curso, 'ucs': ucs}
    return render(request, 'Vitae/detalhes_curso.html', context)


def detalhes_uc(request, acronimo):
    uc = get_object_or_404(UC, acronimo=acronimo)
    planos_curriculares = PlanoCurricular.objects.filter(uc=uc)
    equipa = EquipaDocente.objects.filter(uc=uc)

    context = {'uc': uc, 'planos_curriculares': planos_curriculares, 'equipa': equipa}
    return render(request, 'Vitae/detalhes_uc.html', context)


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
