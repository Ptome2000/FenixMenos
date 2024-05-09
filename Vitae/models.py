from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django_enumfield import enum


class Genero(enum.Enum):
    Masculino = 0
    Feminino = 1
    Outro = 2


class TipoSkills(enum.Enum):
    Hard = 0
    Soft = 1


class EstadoSub(enum.Enum):
    Em_Avaliacao = 0
    Aprovada = 1
    Recusada = 2



class Professor(models.Model):
    numeroProfessor = models.IntegerField(primary_key=True)
    foto = models.ImageField(upload_to='professores', default='', blank=True)
    gabinete = models.CharField(max_length=10)
    #genero = enum.EnumField(Genero, default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + self.user.last_name


class Curso(models.Model):
    codigo = models.CharField(max_length=4, primary_key=True)
    designacao = models.CharField(max_length=100)
    creditos = models.IntegerField()
    descricao = models.TextField()
    coordenador = models.OneToOneField(Professor, on_delete=models.CASCADE)

    def __str__(self):
        return self.designacao


class Skills(models.Model):
    designacao = models.CharField(max_length=100)
    descricao = models.TextField()
    tipo = enum.EnumField(TipoSkills)

    def __str__(self):
        return self.designacao


class UC(models.Model):
    acronimo = models.CharField(max_length=6)
    designacao = models.CharField(max_length=100)
    creditos = models.IntegerField()
    descricao = models.TextField()
    coordenador = models.OneToOneField(Professor, on_delete=models.CASCADE)
    skills = models.ManyToManyField(Skills)

    def __str__(self):
        return self.designacao


class PlanoCurricular(models.Model):
    uc = models.ForeignKey(UC, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    ano = models.IntegerField()
    semestre = models.IntegerField()


class Aluno(models.Model):
    numeroAluno = models.IntegerField(primary_key=True)
    foto = models.ImageField(upload_to='alunos', default='', blank=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    #genero = enum.EnumField(Genero, default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Matricula(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    ano = models.IntegerField()

    def passar_ano(self):
        self.ano = self.ano + 1


class Nota(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    nota = models.IntegerField(validators=[MinValueValidator(10), MaxValueValidator(20)])
    uc = models.ForeignKey(UC, on_delete=models.CASCADE)


class Recomendacao(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    descricao = models.TextField()

'''
class Sugestao(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assunto = models.CharField(max_length=100)
    descricao = models.TextField()
    data = models.DateField(auto_now_add=True)
    estado = enum.EnumField(EstadoSub)
'''