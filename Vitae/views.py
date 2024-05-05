from django.shortcuts import render, get_object_or_404
from .models import Aluno, Professor, Skills, UC, Curso, Nota, Recomendacao, PlanoCurricular

def perfil(request):
    user = request.user
    context = {}
    if hasattr(user, 'aluno'):
        aluno = get_object_or_404(Aluno, user=user)
        matriculas = aluno.matricula_set.all()
        notas = Nota.objects.filter(aluno=aluno)
        recomendacoes = aluno.recomendacao_set.all()
        curso = aluno.curso
        genero = aluno.user.professor.genero.name  # Acessando o enum pelo nome
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
        recomendacoes = Recomendacao.objects.filter(professor=professor)
        genero = professor.genero.name  # Acessando o enum pelo nome
        gabinete = professor.gabinete
        context = {
            'usuario': professor,
            'genero': genero,
            'gabinete': gabinete,
            'ucs': ucs,
            'recomendacoes': recomendacoes
        }
    return render(request, 'perfil.html', context)

def detalhes_curso(request, codigo):
    curso = get_object_or_404(Curso, codigo=codigo)
    ucs = curso.uc_set.all()
    context = {'curso': curso, 'ucs': ucs}
    return render(request, 'detalhes_curso.html', context)


def detalhes_uc(request, acronimo):
    uc = get_object_or_404(UC, acronimo=acronimo)
    skills = uc.skills.all()
    planos_curriculares = PlanoCurricular.objects.filter(uc=uc).select_related(
        'curso')

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

def detalhes_matricula(request, numero_aluno):
    aluno = get_object_or_404(Aluno, numeroAluno=numero_aluno)
    matriculas = aluno.matricula_set.all()
    context = {
        'aluno': aluno,
        'matriculas': matriculas
    }
    return render(request, 'detalhes_matricula.html', context)
