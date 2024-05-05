from django.urls import include, path
from . import views

urlpatterns = [
    path("perfil", views.perfil, name="perfil"),
    path('curso/detalhes/<str:codigo>/', views.detalhes_curso, name='detalhes_curso'),
    path('uc/detalhes/<str:acronimo>/', views.detalhes_uc, name='detalhes_uc'),
    path('aluno/detalhes_matricula/<int:numero_aluno>/', views.detalhes_matricula, name='detalhes_matricula'),
]