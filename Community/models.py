from django.db import models
from django.contrib.auth.models import User
from django_enumfield import enum

class GrupoCategoria(enum.Enum):
    AEISCTE = 0
    SUPORTE = 1
    ESTUDOS = 2
    INVESTIGAR = 3


class Categoria(models.Model):
    designacao = models.CharField(max_length=50, unique=True)
    descricao = models.TextField()
    logo = models.ImageField(upload_to='Categorias', blank=True)
    grupo = enum.EnumField(GrupoCategoria, default=1)

    def __str__(self):
        return self.designacao

    def last_posted(self):
        posts = self.post_set.get()
        comentario = posts.get_last_commented()
        return comentario

    def get_total_posts(self):
        return self.post_set.count()


class Post(models.Model):
    titulo = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

    def get_user(self):
        return self.user.username

    def get_last_commented_user(self):
        return self.comentario_set.order_by('data').last().user

    def get_last_commented_date(self):
        return self.comentario_set.order_by('data').last().data

    def get_total_comments(self):
        return self.comentario_set.count()


    '''
    
    Sugestão
    Posts podem ser 2 tipos:
        - Discussão (Meramente textos com imagens como opcao)
        - Poll (Terá descricao como o acima, mas terá também a possibilidade de criar opções para as pessoas votarem, os utilizados podem votar sem comentar)
    
    '''


class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    imagem = models.ImageField(upload_to='Comentarios', blank=True, null=True)

    def get_user(self):
        return self.user.username
