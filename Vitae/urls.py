from django.urls import include, path
from . import views

urlpatterns = [
    path("perfil", views.perfil, name="perfil"),
]