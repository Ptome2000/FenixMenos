from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'Community'
urlpatterns = [
    # Community Main Page -> Community/
    path("", views.community, name="community"),
    path("Categoria/<str:categoria_dgn>", views.categoria, name="categoria"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
