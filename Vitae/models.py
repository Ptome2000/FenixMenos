from django.core.exceptions import ValidationError
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
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Curso(models.Model):
    codigo = models.IntegerField(primary_key=True)
    acronimo = models.CharField(max_length=4, unique=True)
    designacao = models.CharField(max_length=100)
    creditos = models.IntegerField()
    descricao = models.TextField()
    coordenador = models.OneToOneField(Professor, on_delete=models.CASCADE)

    def __str__(self):
        return self.designacao

    def get_count_uc(self):
        return PlanoCurricular.objects.filter(curso=self).count()


class Skills(models.Model):
    designacao = models.CharField(max_length=100)
    descricao = models.TextField()
    tipo = enum.EnumField(TipoSkills)

    def __str__(self):
        return self.designacao


class UC(models.Model):
    acronimo = models.CharField(max_length=6, unique=True)
    designacao = models.CharField(max_length=100)
    creditos = models.IntegerField()
    descricao = models.TextField()
    coordenador = models.ForeignKey(Professor, on_delete=models.CASCADE)

    def __str__(self):
        return self.designacao

    def get_count_curso(self):
        return PlanoCurricular.objects.filter(uc=self).count()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        EquipaDocente.objects.get_or_create(uc=self, professor=self.coordenador)

    def get_count_alunos_inscritos(self):
        plano = PlanoCurricular.objects.filter(uc=self)
        count = 0
        for uc in plano:
            count += Matricula.objects.filter(curso=uc.curso, ano=uc.ano).count()
        return count


class PlanoCurricular(models.Model):
    uc = models.ForeignKey(UC, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    ano = models.IntegerField()
    semestre = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['uc', 'curso'], name='unique_plano_curricular'),
        ]

    def __str__(self):
        return self.curso.designacao + " - " + self.uc.designacao


class EquipaDocente(models.Model):
    uc = models.ForeignKey(UC, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['uc', 'professor'], name='unique_equipe_docente'),
        ]


class Aluno(models.Model):
    numeroAluno = models.IntegerField(primary_key=True)
    foto = models.ImageField(upload_to='alunos', default='', blank=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.IntegerField(blank=True, null=True)
    morada = models.CharField(max_length=20, blank=True, null=True)
    instagram = models.CharField(max_length=20, blank=True, null=True)
    github = models.CharField(max_length=20, blank=True, null=True)
    facebook = models.CharField(max_length=20, blank=True, null=True)
    data_de_nascimento = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Matricula(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    ano = models.IntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['curso', 'aluno'], name='unique_matricula'),
        ]

    def passar_ano(self):
        self.ano = self.ano + 1

    def __str__(self):
        return str(self.aluno.numeroAluno) + " - " + self.curso.designacao

    def get_media(self):
        planos = PlanoCurricular.objects.filter(curso=self.curso)
        ucs = []
        for uc in planos:
            ucs.append(uc.uc)
        notas = Nota.objects.filter(aluno=self.aluno, uc__in=ucs)
        count_nota = 0
        count_creditos = 0
        for nota in notas:
            creds = nota.uc.creditos
            count_nota += (nota.nota * creds)
            count_creditos += creds
        return count_nota / count_creditos


class Nota(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    nota = models.IntegerField(validators=[MinValueValidator(10), MaxValueValidator(20)], null=True, blank=True)
    uc = models.ForeignKey(UC, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.aluno.numeroAluno) + " - " + str(self.uc) + "(" + str(self.nota) + ")"




'''
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        planos = PlanoCurricular.objects.filter(uc=self.uc)
        cursos = []
        ucs = []
        for curso in planos:
            cursos.append(curso.curso)
        for uc in planos:
            ucs.append(uc.uc)
        matricula = Matricula.objects.filter(aluno=self.aluno, curso__in=cursos)
        notas = self.objects.filter(aluno=matricula.aluno, uc__in=ucs)
        count_creditos = 0
        for nota in notas:
            creds = nota.uc.creditos
            count_creditos += creds
        credits_per_year = matricula.curso.creditos / matricula.curso.anos
'''


class UC_Skills(models.Model):
    skills = models.ForeignKey(Skills, on_delete=models.CASCADE)
    uc = models.ForeignKey(UC, on_delete=models.CASCADE)
    nivel = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['skills', 'uc'], name='unique_UC_Skills'),
        ]

    def clean(self):
        if self.skills.tipo != 0 and self.nivel is not None:
            raise ValidationError("Nível só pode ser definido para skills do tipo 'Hard'.")


class UC_Skills_Aluno(models.Model):
    alunOo = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    uc_skills = models.ForeignKey(UC_Skills, on_delete=models.CASCADE)
    progresso = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)

    def clean(self):
        if self.uc_skills.skills.tipo != 0 and self.progresso is not None:
            raise ValidationError("Progresso só pode ser definido para skills do tipo 'Hard'.")


class Projecto(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50)
    data = models.DateField()
    descricao = models.TextField()


class Certificacao(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50)
    url = models.URLField()


class Recomendacao(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    descricao = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['aluno', 'professor'], name='unique_recomendacao'),
        ]


class Sugestao(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='avaliado_por', null=True, default=None,
                              blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sugerido_por')
    assunto = models.CharField(max_length=100)
    descricao = models.TextField()
    data = models.DateField(auto_now_add=True)
    estado = enum.EnumField(EstadoSub, default=0)

    def clean(self):
        if self.admin and not self.admin.is_superuser:
            raise ValidationError("Para avaliar sugestões, é necessário ser administrador")
