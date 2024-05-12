from django.urls import include, path
from . import views
from .views import salvar_perfil

app_name = 'Vitae'

urlpatterns = [
    path("perfil", views.perfil, name="perfil"),
    path('Curso/<str:acronimo>/', views.detalhes_curso, name='detalhes_curso'),
    path('UC/<str:acronimo>/', views.detalhes_uc, name='detalhes_uc'),
    path('fazer_upload/', views.fazer_upload, name='fazer_upload'),
    path('UC/Listagem', views.UnidadesCurriculares, name='UnidadesCurriculares'),
    path('UC/<str:acronimo>/Alunos', views.alunosInscritos, name='alunosInscritos'),
    path('salvar_perfil/', salvar_perfil, name='salvar_perfil'),
    path('cv/<str:utilizador_id>/', views.detalhes_cv, name='cv'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
]