from django.db import models
from django.contrib.auth.models import User
from django_enumfield import enum

class GrupoCategoria(enum.Enum):
    AEISCTE = 0
    SUPORTE = 1
    ESTUDOS = 2
    INVESTIGAR = 3


class Categoria(models.Model):
    designacao = models.CharField(max_length=50)
    descricao = models.TextField()
    logo = models.ImageField(upload_to='Categorias', null=False)
    postagens = models.IntegerField(default=0)
    grupo = enum.EnumField(GrupoCategoria, default=1)

    def __str__(self):
        return self.designacao

    def last_posted(self):
        return self.post_set.order_by('-data').last()


class Post(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='posts', null=True)
    comentarios = models.IntegerField(default=0)

    def get_user(self):
        return self.user.username

    def get_last_commented(self):
        return self.comentario_set.order_by('data').last()


class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    imagem = models.ImageField(upload_to='comentarios', null=True)

    def get_user(self):
        return self.user.username
