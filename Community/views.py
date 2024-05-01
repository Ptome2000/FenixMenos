from django.shortcuts import render, get_object_or_404

from Community.models import Categoria


def community(request):
    lista_categorias = Categoria.objects.all()
    context = {'lista_categorias': lista_categorias}
    return render(request, "community/community.html", context)


def categoria(request, categoria_dgn):
    categoria = get_object_or_404(Categoria, designacao=categoria_dgn)
    return render(request, 'community/categoria.html', {'categoria': categoria, })
