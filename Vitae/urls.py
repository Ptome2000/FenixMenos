from django.urls import include, path
from . import views

urlpatterns = [
    path("perfil", views.perfil, name="perfil"),
    path('Vitae/fazer_upload', views.fazer_upload, name='fazer_upload'),
]