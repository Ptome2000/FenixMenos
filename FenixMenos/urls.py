"""
URL configuration for FenixMenos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djayangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from serializers import CursoViewSet
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import RegistoAluno

router = DefaultRouter()
router.register(r'cursos', CursoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Vitae/', include('Vitae.urls')),
    path('', views.index, name='index'),
    path('Community/', include('Community.urls')),
    path("FenixMenos/", views.index, name="index"),
    path("FenixMenos/login", views.loginform, name="login"),
    path("FenixMenos/registar", views.registo, name="registo"),
    path("FenixMenos/logout", views.logoutForm, name="logout"),
    path('api/', include(router.urls)),
    path('register/', RegistoAluno, name='register'),
    path('FenixMenos/sugestoes', views.sugestoes, name="sugestoes"),
    path('FenixMenos/registar-professor', views.registarProf, name="registarProfessor"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
