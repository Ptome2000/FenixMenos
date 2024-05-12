from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from .models import *
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Aluno


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


def detalhes_cv(request, utilizador_id):
    global uc_skills_aluno_corrente
    user = get_object_or_404(User, pk=utilizador_id)

    try:
        aluno = user.aluno
        uc_skills_aluno_corrente = UC_Skills_Aluno.objects.filter(alunOo_id=aluno.numeroAluno)


    except Aluno.DoesNotExist:
        aluno = None

    if aluno:

        alunotest = user
        context = {'aluno': alunotest, 'uc_skills_aluno': uc_skills_aluno_corrente}
    else:
        context = {'error': 'No aluno profile found for this user.'}

    return render(request, 'Vitae/cv.html', context)


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
        n, created = Nota.objects.get_or_create(aluno_id=aluno.numeroAluno, uc=uc)
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
    if request.method == 'POST' and request.FILES.get('myfile'):
        myfile = request.FILES['myfile']
        aluno = Aluno.objects.filter(user=user).first()
        professor = Professor.objects.filter(user=user).first()
        if aluno:
            aluno.avatar = myfile
            aluno.save()
            messages.success(request, "Foto carregada com sucesso!")
        elif professor:
            professor.avatar = myfile
            professor.save()
            messages.success(request, "Foto carregada com sucesso!")
        else:
            messages.error(request, "Perfil não encontrado.")

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


@login_required
def editar_perfil(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        messages.success(request, "Perfil atualizado com sucesso!")
        return redirect('Vitae:perfil')
    else:
        return render(request, 'Vitae/editar_perfil.html', {'user': request.user})
