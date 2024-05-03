from django.shortcuts import render, get_object_or_404
from Community.models import *


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
    lista_comentarios = Comentario.objects.filter(post=post_Id)
    context = {'post': post, 'lista_comentarios': lista_comentarios, 'categoria': categoria}
    return render(request, 'community/post.html', context)


def criarPost(request, categoria_dgn):
    if request.method == 'GET':
        categoria = get_object_or_404(Categoria, designacao=categoria_dgn)
        return render(request, 'community/novoPost.html', {'categoria': categoria})
    else:
        titulo = request.POST['titulo']