from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'Community'
urlpatterns = [
    # Community Main Page -> Community/
    path("", views.community, name="community"),
    path("Categoria/<str:categoria_dgn>", views.categoria, name="categoria"),
    path("Categoria/<str:categoria_dgn>/<int:post_Id>", views.post, name="post"),
    path("Categoria/<str:categoria_dgn>/Novo-Post", views.criarPost, name="criarPost"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
