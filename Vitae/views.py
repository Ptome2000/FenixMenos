import os

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, FileResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from .models import *
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from FenixMenos.views import is_professor, is_aluno
import subprocess
from django.http import HttpResponse


@login_required(login_url='login')
def perfil(request):
    user = request.user
    context = {'user': user}
    return render(request, 'Vitae/perfil.html', context)


@login_required(login_url='login')
def detalhes_curso(request, acronimo):
    curso = get_object_or_404(Curso, acronimo=acronimo)
    planos_curriculares = PlanoCurricular.objects.filter(curso=curso).order_by('ano')
    context = {'curso': curso, 'planos_curriculares': planos_curriculares}
    return render(request, 'Vitae/detalhes_curso.html', context)


@login_required(login_url='login')
def detalhes_uc(request, acronimo):
    try:
        uc = get_object_or_404(UC, acronimo=acronimo)
        planos_curriculares = PlanoCurricular.objects.filter(uc=uc)
        equipa = EquipaDocente.objects.filter(uc=uc)

        context = {'uc': uc, 'planos_curriculares': planos_curriculares, 'equipa': equipa}
        return render(request, 'Vitae/detalhes_uc.html', context)
    except KeyError:
        messages.warning(request, "Ocorreu um erro durante o seu pedido")
        return HttpResponseRedirect(reverse('FenixMenos'))


def detalhes_cv(request, utilizador):
    global uc_skills_aluno_corrente, certificacoes, projectos, recomendacoes
    user = get_object_or_404(User, username=utilizador)

    try:
        aluno = user.aluno
        uc_skills_aluno_corrente = UC_Skills_Aluno.objects.filter(alunOo_id=aluno.numeroAluno)
        certificacoes = Certificacao.objects.filter(aluno=aluno.numeroAluno)
        projectos = Projecto.objects.filter(aluno=aluno.numeroAluno)
        recomendacoes = Recomendacao.objects.filter(aluno=aluno.numeroAluno)

    except Aluno.DoesNotExist:
        aluno = None

    if aluno:

        alunotest = user
        context = {'aluno': alunotest, 'uc_skills_aluno': uc_skills_aluno_corrente, 'certificacoes': certificacoes,
                   'projectos': projectos, 'recomendacoes': recomendacoes}
    else:
        context = {'error': 'No aluno profile found for this user.'}

    return render(request, 'Vitae/cv.html', context)


def detalhes_cvpdf(request, utilizador):
    global uc_skills_aluno_corrente, certificacoes, projectos
    user = get_object_or_404(User, username=utilizador)

    try:
        aluno = user.aluno
        uc_skills_aluno_corrente = UC_Skills_Aluno.objects.filter(alunOo_id=aluno.numeroAluno)
        certificacoes = Certificacao.objects.filter(aluno=aluno.numeroAluno)
        projectos = Projecto.objects.filter(aluno=aluno.numeroAluno)


    except Aluno.DoesNotExist:
        aluno = None

    if aluno:

        alunotest = user
        context = {'aluno': alunotest, 'uc_skills_aluno': uc_skills_aluno_corrente, 'certificacoes': certificacoes,
                   'projectos': projectos}
    else:
        context = {'error': 'No aluno profile found for this user.'}

    return render(request, 'Vitae/cv_pdf.html', context)


@user_passes_test(is_professor, login_url=reverse_lazy('index'))
def UnidadesCurriculares(request):
    try:
        unidades = EquipaDocente.objects.filter(professor=request.user.professor)
        context = {'unidades': unidades}
        return render(request, 'Vitae/listar_prof_uc.html', context)
    except KeyError:
        messages.warning(request, "Ocorreu um erro durante o seu pedido")
    return HttpResponseRedirect(reverse('FenixMenos'))


@user_passes_test(is_professor, login_url=reverse_lazy('index'))
def alunosInscritos(request, acronimo):
    try:
        uc = get_object_or_404(UC, acronimo=acronimo)
        if request.method == 'POST':
            aluno = Aluno.objects.get(numeroAluno=request.POST.get('aluno'))
            nota = request.POST.get('nota')
            n, created = Nota.objects.get_or_create(aluno_id=aluno.numeroAluno, uc=uc)
            n.nota = nota
            n.save()
            if created:
                uc_skills = UC_Skills.objects.filter(uc=uc)
                for uc_skill in uc_skills:
                    if uc_skill.skills.tipo == 0:
                        max_grade = Nota.objects.filter().aggregate(Max('nota'))['nota__max']
                        progresso = (int(n.nota) / max_grade) * uc_skill.nivel
                        UC_Skills_Aluno.objects.update_or_create(
                            alunOo_id=aluno.numeroAluno,
                            uc_skills=uc_skill,
                            defaults={'progresso': progresso}
                        )
                    else:
                        UC_Skills_Aluno.objects.update_or_create(
                            alunOo_id=aluno.numeroAluno,
                            uc_skills=uc_skill,
                            defaults={'progresso': 0}
                        )
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
    except KeyError:
        messages.warning(request, "Ocorreu um erro durante o seu pedido")
        return HttpResponseRedirect(reverse('FenixMenos'))


@login_required(login_url='login')
def fazer_upload(request):
    if request.method == 'POST' and request.FILES.get('myfile'):
        myfile = request.FILES['myfile']
        aluno = Aluno.objects.filter(user=request.user).first()
        professor = Professor.objects.filter(user=request.user).first()
        if aluno:
            aluno.foto = myfile
            aluno.save()
            messages.success(request, "Foto de perfil atualizada com sucesso!")

        elif professor:
            professor.foto = myfile
            professor.save()
            messages.success(request, "Foto de perfil atualizada com sucesso!")
        else:
            messages.error(request, "Perfil não encontrado")

        return redirect('Vitae:perfil')
    else:
        messages.error(request, "Nenhum arquivo foi enviado.")
        return redirect('Vitae:perfil')


@login_required(login_url='login')
def salvar_perfil(request):
    try:
        if request.method == 'POST':
            user = request.user
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.email = request.POST.get('email', '')
            user.gabinete = request.POST.get('gabinete', '')
            user.save()
            return redirect('Vitae:perfil')
    except KeyError:
        messages.warning(request, "Ocorreu um erro durante o seu pedido")
        return HttpResponseRedirect(reverse('FenixMenos'))


@login_required(login_url='login')
def editar_perfil(request):
    try:
        if request.method == 'POST':
            user = request.user
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.email = request.POST.get('email', '@iscte.pt')
            if not user.email:
                messages.error(request, " O Email é obrigatório")
                return render(request, 'Vitae/editar_perfil.html', {'user': request.user})
            aluno = Aluno.objects.filter(user=request.user).first()
            professor = Professor.objects.filter(user=request.user).first()
            if professor:
                professor.gabinete = request.POST.get('gabinete', '')
                professor.save()
            elif aluno:
                aluno.instagram = request.POST.get('instagram', '') or None
                aluno.data_de_nascimento = request.POST.get('data_de_nascimento', '') or None
                aluno.morada = request.POST.get('morada', '') or None
                aluno.github = request.POST.get('github', '') or None
                aluno.telefone = request.POST.get('telefone', '') or '000000000'
                aluno.facebook = request.POST.get('facebook', '') or None
                aluno.save()
            user.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('Vitae:perfil')
        else:
            return render(request, 'Vitae/editar_perfil.html', {'user': request.user})
    except KeyError:
        messages.warning(request, "Ocorreu um erro durante o seu pedido")
        return HttpResponseRedirect(reverse('FenixMenos'))


@user_passes_test(is_professor, login_url=reverse_lazy('index'))
def recomendar(request, numeroAluno):
    try:
        aluno = Aluno.objects.get(numeroAluno=numeroAluno)
        if request.method == 'POST':
            recomendacao = request.POST.get('recomendacao')
            professor = Professor.objects.get(user=request.user)
            Recomendacao.objects.create(aluno=aluno, descricao=recomendacao, professor=professor)
            messages.success(request, 'Recomendação feita com sucesso')
            return HttpResponseRedirect(reverse('Vitae:cv', args=[aluno.user.username]))
        else:
            return render(request, 'Vitae/recomendar.html', {'aluno': aluno})
    except KeyError:
        messages.warning(request, "Ocorreu um erro durante o seu pedido")
        return HttpResponseRedirect(reverse('FenixMenos'))


@user_passes_test(is_aluno, login_url=reverse_lazy('index'))
def certficacaoprojecto(request):
    try:
        if request.method == 'POST':
            aluno = request.user.aluno  # Assumindo que Aluno tem uma relação OneToOne com User
            if 'add_certificacao' in request.POST:
                nome = request.POST.get('nome_cert')
                url = request.POST.get('url_cert')
                if nome and url:
                    Certificacao.objects.create(aluno=aluno, nome=nome, url=url)

            elif 'add_projecto' in request.POST:
                nome = request.POST.get('nome_proj')
                data = request.POST.get('data_proj')
                descricao = request.POST.get('descricao_proj')
                if nome and data and descricao:
                    Projecto.objects.create(aluno=aluno, nome=nome, data=data, descricao=descricao)

            return HttpResponseRedirect(request.path_info)

        certificacoes = Certificacao.objects.filter(aluno=request.user.aluno)
        projetos = Projecto.objects.filter(aluno=request.user.aluno)
        return render(request, 'Vitae/certificacaoprojecto.html', {
            'certificacoes': certificacoes,
            'projetos': projetos
        })
    except KeyError:
        messages.warning(request, "Ocorreu um erro durante o seu pedido")
        return HttpResponseRedirect(reverse('FenixMenos'))


@login_required(login_url='login')
def listarAlunos(request):
    try:
        pesquisa = request.GET.get('search')
        if pesquisa:
            aluno = Aluno.objects.filter(user__first_name__contains=pesquisa)
            matriculados = Matricula.objects.filter(aluno__in=aluno)
            return render(request, 'Vitae/listar_alunos.html', {'matriculados': matriculados})
        else:
            matriculados = Matricula.objects.all()
            return render(request, 'Vitae/listar_alunos.html', {'matriculados': matriculados})
    except KeyError:
        messages.warning(request, "Ocorreu um erro com o seu pedido")
        return HttpResponseRedirect(reverse('FenixMenos'))


@login_required(login_url='login')
def pesquisarAlunos(request):
    try:
        pesquisa = request.POST.get('pesquisa')
        user = User.objects.filter(first_name__contains=pesquisa)
        matriculados = Matricula.objects.filter(user__in=user)
        return render(request, 'Vitae/listar_alunos.html', {'matriculados': matriculados})
    except KeyError:
        messages.warning(request, "Ocorreu um erro com o seu pedido")
        return HttpResponseRedirect(reverse('FenixMenos'))


@login_required(login_url='login')
def listarCursos(request):
    try:
        cursos = Curso.objects.all()
        return render(request, 'Vitae/listar_cursos.html', {'cursos': cursos})
    except KeyError:
        messages.warning(request, "Ocorreu um erro com o seu pedido")
        return HttpResponseRedirect(reverse('FenixMenos'))


def generate_pdf_view(request, utilizador):
    try:
        # Caminho para o seu script Node.js
        script_path = 'node_app/generatePdf.js'
        pdf_output_path = 'output.pdf'

        url = 'http://localhost:8000/Vitae/cv/' + utilizador + 'cvpdf'

        if os.path.exists(script_path):
            # Chamar o script Node.js
            result = subprocess.run(['node', script_path, url, pdf_output_path], capture_output=True, text=True)

            if result.returncode == 0:
                try:
                    pdf_file = open(pdf_output_path, 'rb')
                    response = FileResponse(pdf_file, as_attachment=True, filename='downloaded_pdf.pdf')
                    response['Content-Type'] = 'application/pdf'
                    response['Content-Disposition'] = f'attachment; filename="{utilizador}_downloaded_pdf.pdf"'
                    return response
                except Exception as e:
                    return HttpResponse(f"Erro ao abrir o PDF: {str(e)}", status=500)
            else:
                return HttpResponse(f"Falha ao gerar PDF: {result.stderr}", status=500)
        else:
            return HttpResponse("Script de geração de PDF não encontrado.", status=404)
    except KeyError:
        messages.warning(request, "Ocorreu um erro durante o seu pedido")
        return HttpResponseRedirect(reverse('FenixMenos'))
