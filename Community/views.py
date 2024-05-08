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
    categoria = get_object_or_404(Categoria, designacao=categoria_dgn)
    lista_posts = Post.objects.filter(categoria=categoria)
    context = {'categoria': categoria, 'lista_posts': lista_posts}
    return render(request, 'community/categoria.html', context)


def post(request, categoria_dgn, post_Id):
    categoria = get_object_or_404(Categoria, designacao=categoria_dgn)
    post = get_object_or_404(Post, id=post_Id)
    try:
        if request.method == 'POST' and 'action' in request.POST:
            action = request.POST['action']
            if action == 'Apagar':
                post.delete()
                messages.success(request, 'Tópico apagado com sucesso')
                return HttpResponseRedirect(reverse('Community:categoria', args=[categoria.designacao]))
            elif action == 'ApagarLista':
                selected = request.POST.getlist('selectedPost')
                request.session['commentsToDelete'] = selected
                return HttpResponseRedirect(reverse('Community:apagarComentarios', args=[post.id]))
            elif action == 'Responder':
                texto = request.POST.get('message')
                imagem = request.POST.get('ImageFile')
                Comentario.objects.create(post=post, user=request.user, texto=texto, data=dt.datetime.now(), imagem=imagem)
                messages.success(request, 'Resposta publicada com sucesso')

        context = {'post': post, 'categoria': categoria}
        return render(request, 'community/post.html', context)
    except KeyError:
        messages.warning(request, "Ocorreu um erro com o seu pedido")
        return HttpResponseRedirect(reverse('Community:community'))


def criarDiscussao(request, categoria_dgn):
    categoria = get_object_or_404(Categoria, designacao=categoria_dgn)
    try:
        if request.method == 'POST':
            titulo = request.POST.get('title')
            texto = request.POST.get('message')
            imagem = request.POST.get('ImageFile')
            post = Post.objects.create(titulo=titulo, categoria=categoria, user=request.user)
            Comentario.objects.create(post=post, user=request.user, texto=texto, data=dt.datetime.now(), imagem=imagem)
            messages.success(request, 'Tópico criado com sucesso')
            return HttpResponseRedirect(reverse('Community:post', args=[categoria.designacao, post.id]))
        else:
            return render(request, 'community/novaDiscussion.html', {'categoria': categoria})
    except KeyError:
        messages.warning(request, "Ocorreu um erro com o seu pedido")
        return HttpResponseRedirect(reverse('Community:categoria', args=[categoria.designacao]))


def criarVotacao(request, categoria_dgn):
    categoria = get_object_or_404(Categoria, designacao=categoria_dgn)
    messages.warning(request, "Recurso a ser implementado em breve. Pedimos desculpa pelo incómodo")
    return HttpResponseRedirect(reverse('Community:categoria', args=[categoria.designacao]))


def apagarComentarios(request, post_Id):
    post = get_object_or_404(Post, id=post_Id)
    try:
        selected = request.session.get('commentsToDelete')
        if request.method == 'POST':
            for c in selected:
                comentario = Comentario.objects.get(id=c)
                post.comentario_set.get(id=comentario.id).delete()
            messages.warning(request, "Comentários apagado com sucesso")
            return HttpResponseRedirect(reverse('Community:post', args=[post.categoria.designacao, post.id]))
        else:
            comentarios = post.comentario_set.filter(pk__in=selected)
            context = {'post': post, 'comentarios': comentarios}
            return render(request, 'community/apagarComentarios.html', context)
    except KeyError:
        messages.warning(request, "Ocorreu um erro com o seu pedido")
        return HttpResponseRedirect(reverse('Community:categoria', args=[post.categoria.designacao]))
