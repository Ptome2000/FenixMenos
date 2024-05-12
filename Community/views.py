import datetime as dt
from django.shortcuts import render, get_object_or_404
from Community.models import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages


def community(request):
    grupos = GrupoCategoria.items()
    lista_categorias = Categoria.objects.all()
    context = {'lista_categorias': lista_categorias, 'grupos_categorias': grupos}
    return render(request, "community/community.html", context)


def categoria(request, categoria_dgn):
    c = get_object_or_404(Categoria, designacao=categoria_dgn)
    lista_posts = Post.objects.filter(categoria=c)
    context = {'categoria': c, 'lista_posts': lista_posts}
    return render(request, 'community/categoria.html', context)


def post(request, categoria_dgn, post_Id):
    c = get_object_or_404(Categoria, designacao=categoria_dgn)
    p = get_object_or_404(Post, id=post_Id)
    try:
        if request.method == 'POST' and 'action' in request.POST:
            action = request.POST['action']
            if action == 'Apagar':
                p.delete()
                messages.success(request, 'Tópico apagado com sucesso')
                return HttpResponseRedirect(reverse('Community:categoria', args=[c.designacao]))
            elif action == 'ApagarLista':
                selected = request.POST.getlist('selectedPost')
                request.session['commentsToDelete'] = selected
                return HttpResponseRedirect(reverse('Community:apagarComentarios', args=[p.id]))
            elif action == 'Responder':
                texto = request.POST.get('message')
                imagem = request.FILES.get('ImageFile')
                Comentario.objects.create(post=p, user=request.user, texto=texto, data=dt.datetime.now(), imagem=imagem)
                messages.success(request, 'Resposta publicada com sucesso')

        context = {'post': p, 'categoria': c}
        return render(request, 'community/post.html', context)
    except KeyError:
        messages.warning(request, "Ocorreu um erro com o seu pedido")
        return HttpResponseRedirect(reverse('Community:community'))


def criarDiscussao(request, categoria_dgn):
    c = get_object_or_404(Categoria, designacao=categoria_dgn)
    try:
        if request.method == 'POST':
            titulo = request.POST.get('title')
            texto = request.POST.get('message')
            imagem = request.FILES.get('ImageFile')
            p = Post.objects.create(titulo=titulo, categoria=c, user=request.user)
            Comentario.objects.create(post=p, user=request.user, texto=texto, data=dt.datetime.now(), imagem=imagem)
            messages.success(request, 'Tópico criado com sucesso')
            return HttpResponseRedirect(reverse('Community:post', args=[c.designacao, p.id]))
        else:
            return render(request, 'community/novaDiscussion.html', {'categoria': c})
    except KeyError:
        messages.warning(request, "Ocorreu um erro com o seu pedido")
        return HttpResponseRedirect(reverse('Community:categoria', args=[c.designacao]))


def criarVotacao(request, categoria_dgn):
    c = get_object_or_404(Categoria, designacao=categoria_dgn)
    messages.warning(request, "Recurso a ser implementado em breve. Pedimos desculpa pelo incómodo")
    return HttpResponseRedirect(reverse('Community:categoria', args=[c.designacao]))


def criarCategoria(request):
    try:
        if request.method == 'POST':
            designacao = request.POST.get('designacao')
            descricao = request.POST.get('descricao')
            logo = request.FILES.get('ImageFile')
            grupo = int(request.POST.get('grupo'))
            Categoria.objects.create(designacao=designacao, descricao=descricao, logo=logo, grupo=grupo)
            messages.success(request, 'Categoria criada com sucesso')
            return HttpResponseRedirect(reverse('Community:categoria', args=[designacao]))
        else:
            grupos = GrupoCategoria.items()
            return render(request, 'community/criar_categoria.html', context={'grupos': grupos})
    except KeyError:
        messages.warning(request, "Ocorreu um erro com o seu pedido")
        return HttpResponseRedirect(reverse('Community:community'))


def apagarComentarios(request, post_Id):
    p = get_object_or_404(Post, id=post_Id)
    try:
        selected = request.session.get('commentsToDelete')
        if request.method == 'POST':
            first = p.comentario_set.first()
            count = 0
            for c in selected:
                c = Comentario.objects.get(id=c)
                if c == first:
                    messages.warning(request, 'Erro: Tentou apagar o primeiro comentário')
                else:
                    p.comentario_set.get(id=c.id).delete()
                    count += 1
            if count > 0:
                messages.success(request, str(count) + " comentários apagado com sucesso")
            return HttpResponseRedirect(reverse('Community:post', args=[p.categoria.designacao, p.id]))
        else:
            c = p.comentario_set.filter(pk__in=selected)
            context = {'post': p, 'comentarios': c}
            return render(request, 'community/apagarComentarios.html', context)
    except KeyError:
        messages.warning(request, "Ocorreu um erro com o seu pedido")
        return HttpResponseRedirect(reverse('Community:categoria', args=[p.categoria.designacao]))
