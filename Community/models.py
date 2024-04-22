from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    designacao = models.CharField(max_length=50)
    descricao = models.TextField()

    def __str__(self):
        return self.designacao


class Post(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_user(self):
        return self.user.username


class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

    def get_user(self):
        return self.user.username
