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


def detalhes_curso(request, acronimo):
    curso = get_object_or_404(Curso, acronimo=acronimo)
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


def alunosInscritos(request, acronimo):
    uc = get_object_or_404(UC, acronimo=acronimo)
    if request.method == 'POST':
        aluno = Aluno.objects.get(numeroAluno=request.POST.get('aluno'))
        nota = request.POST.get('nota')
        n, created = Nota.objects.get_or_create(aluno=aluno, uc=uc)
        n.nota = nota
        n.save()
        if created:
            messages.success(request, "Aluno " + aluno.user.first_name + " avaliado com sucesso!")
        else:
            messages.success(request, "Nota do aluno " + aluno.user.first_name + " atualizada com sucesso!")
    planos = PlanoCurricular.objects.filter(uc=uc).values('curso_id')
    anos = PlanoCurricular.objects.filter(uc=uc).values('ano')
    matriculas = Matricula.objects.filter(curso__in=planos, ano__in=anos).distinct()
    notas = Nota.objects.filter(uc=uc).distinct()
    nota_dict = {}
    for nota in notas:
        nota_dict[nota.aluno.numeroAluno] = nota.nota
    alunos = []
    for matricula in matriculas:
        student_info = {
            'aluno': matricula.aluno,
            'curso': matricula.curso,
            'nota': nota_dict.get(matricula.aluno.numeroAluno, None)
        }
        alunos.append(student_info)

    context = {'alunos': alunos, 'uc': uc}
    return render(request, 'Vitae/listar_alunos_uc.html', context)


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


@login_required
def salvar_perfil(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        # Redirecionar para alguma página de sucesso ou de volta ao perfil
        return redirect('Vitae:perfil')



