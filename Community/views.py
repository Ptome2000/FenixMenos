from django.shortcuts import render, get_object_or_404

from Community.models import Categoria, Post


def community(request):
    lista_categorias = Categoria.objects.all()
    context = {'lista_categorias': lista_categorias}
    return render(request, "community/community.html", context)


def categoria(request, categoria_dgn):
    categoria = get_object_or_404(Categoria, designacao=categoria_dgn)
    lista_posts = Post.objects.filter(categoria=categoria)
    return render(request, 'community/categoria.html', {'categoria': categoria, 'lista_posts': lista_posts})
