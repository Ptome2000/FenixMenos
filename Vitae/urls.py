from django.urls import include, path
from . import views
app_name = 'Vitae'
urlpatterns = [
    path("perfil", views.perfil, name="perfil"),
    path('curso/<str:codigo>/', views.detalhes_curso, name='detalhes_curso'),
    path('uc/<str:acronimo>/', views.detalhes_uc, name='detalhes_uc'),
    path('fazer_upload/', views.fazer_upload, name='fazer_upload'),
]