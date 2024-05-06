from datetime import datetime
from django.shortcuts import render, get_object_or_404
from Community.models import *
from django.http import HttpResponseRedirect
from django.urls import reverse


def community(request):
    grupos_categorias = GrupoCategoria.items()
    lista_categorias = Categoria.objects.all()
    context = {'lista_categorias': lista_categorias, 'grupos_categorias': grupos_categorias}
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
        if request.method == 'POST':
            texto = request.POST.get('message')
            imagem = request.POST.get('ImageFile')
            Comentario.objects.create(post=post, user=request.user, texto=texto, data=datetime.now(), imagem=imagem)

            # ADICIONAR MENSAGEM DE SUCESSO

        lista_comentarios = Comentario.objects.filter(post=post_Id)
        context = {'post': post, 'lista_comentarios': lista_comentarios, 'categoria': categoria}
        return render(request, 'community/post.html', context)
    except KeyError:

        # ADICIONAR MENSAGEM DE ERRO

        return render(request, '')


def criarDiscussao(request, categoria_dgn):
    categoria = get_object_or_404(Categoria, designacao=categoria_dgn)
    if request.method == 'GET':
        return render(request, 'community/novaDiscussion.html', {'categoria': categoria})
    else:
        try:
            titulo = request.POST['title']
            texto = request.POST['message']
            imagem = request.POST['ImageFile']
            post = Post.objects.create(titulo=titulo, categoria=categoria, user=request.user)
            Comentario.objects.create(post=post, user=request.user, texto=texto, data=datetime.now(), imagem=imagem)
        except KeyError:
            return HttpResponseRedirect(reverse('Community:categoria', args=(categoria)))


def criarVotacao(request, categoria_dgn):
    categoria = get_object_or_404(Categoria, designacao=categoria_dgn)
    if request.method == 'GET':
        return render(request, 'community/novaDiscussion.html', {'categoria': categoria})
    else:
        try:
            titulo = request.POST['title']
            texto = request.POST['message']
            imagem = request.POST['ImageFile']
            post = Post(titulo=titulo, texto=texto, imagem=imagem)
        except KeyError:
            return render(request, '')
        else:
            return HttpResponseRedirect(reverse('Community:categoria', args=(categoria)))