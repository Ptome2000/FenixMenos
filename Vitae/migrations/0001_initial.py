# Generated by Django 5.0.4 on 2024-04-22 17:59

import Vitae.models
import django.core.validators
import django.db.models.deletion
import django_enumfield.db.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('codigo', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('designacao', models.CharField(max_length=100)),
                ('creditos', models.IntegerField()),
                ('descricao', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designacao', models.CharField(max_length=100)),
                ('descricao', models.TextField()),
                ('tipo', django_enumfield.db.fields.EnumField(enum=Vitae.models.TipoSkills)),
            ],
        ),
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('numeroAluno', models.IntegerField(primary_key=True, serialize=False)),
                ('foto', models.ImageField(upload_to='alunos')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Vitae.curso')),
            ],
        ),
        migrations.CreateModel(
            name='Matricula',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ano', models.IntegerField()),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Vitae.aluno')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Vitae.curso')),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('numeroProfessor', models.IntegerField(primary_key=True, serialize=False)),
                ('foto', models.ImageField(upload_to='professores')),
                ('gabinete', models.CharField(max_length=10)),
                ('genero', django_enumfield.db.fields.EnumField(enum=Vitae.models.Genero)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='curso',
            name='coordenador',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Vitae.professor'),
        ),
        migrations.CreateModel(
            name='Recomendacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.TextField()),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Vitae.aluno')),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Vitae.professor')),
            ],
        ),
        migrations.CreateModel(
            name='UC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acronimo', models.CharField(max_length=6)),
                ('designacao', models.CharField(max_length=100)),
                ('creditos', models.IntegerField()),
                ('descricao', models.TextField()),
                ('coordenador', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Vitae.professor')),
                ('skills', models.ManyToManyField(to='Vitae.skills')),
            ],
        ),
        migrations.CreateModel(
            name='PlanoCurricular',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ano', models.IntegerField()),
                ('semestre', models.IntegerField()),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Vitae.curso')),
                ('uc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Vitae.uc')),
            ],
        ),
        migrations.CreateModel(
            name='Nota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota', models.IntegerField(validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(20)])),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Vitae.aluno')),
                ('uc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Vitae.uc')),
            ],
        ),
    ]
