
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Aluno, Professor, Skills, UC, Curso, Nota, Recomendacao, PlanoCurricular, Matricula

def perfil(request):
    user = request.user
    context = {}
    if user.is_authenticated:
        if hasattr(user, 'aluno'):
            aluno = get_object_or_404(Aluno, user=user)
            matriculas = Matricula.objects.filter(aluno=aluno)
            notas = Nota.objects.filter(aluno=aluno)
            recomendacoes = Recomendacao.objects.filter(aluno=aluno)
            curso = aluno.curso
            genero = aluno.user.professor.genero.name
            context = {
                'usuario': aluno,
                'genero': genero,
                'curso': curso,
                'matriculas': matriculas,
                'notas': notas,
                'recomendacoes': recomendacoes
            }
        elif hasattr(user, 'professor'):
            professor = get_object_or_404(Professor, user=user)
            ucs = UC.objects.filter(coordenador=professor)
            genero = professor.genero.name
            gabinete = professor.gabinete
            context = {
                'usuario': professor,
                'genero': genero,
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
    return render(request, 'detalhes_curso.html', context)


def detalhes_uc(request, acronimo):
    uc = get_object_or_404(UC, acronimo=acronimo)
    skills = uc.skills.all()
    planos_curriculares = PlanoCurricular.objects.filter(uc=uc).select_related('curso')

    cursos_info = {}
    for plano in planos_curriculares:
        if plano.curso.designacao not in cursos_info:
            cursos_info[plano.curso.designacao] = []
        cursos_info[plano.curso.designacao].append((plano.ano, plano.semestre))

    context = {
        'uc': uc,
        'skills': skills,
        'planos_curriculares': cursos_info
    }
    return render(request, 'detalhes_uc.html', context)

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
