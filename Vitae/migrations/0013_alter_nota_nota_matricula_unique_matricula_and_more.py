# Generated by Django 5.0.5 on 2024-05-12 00:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vitae', '0012_alter_sugestao_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nota',
            name='nota',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(20)]),
        ),
        migrations.AddConstraint(
            model_name='matricula',
            constraint=models.UniqueConstraint(fields=('curso', 'aluno'), name='unique_matricula'),
        ),
        migrations.AddConstraint(
            model_name='planocurricular',
            constraint=models.UniqueConstraint(fields=('uc', 'curso'), name='unique_plano_curricular'),
        ),
        migrations.AddConstraint(
            model_name='recomendacao',
            constraint=models.UniqueConstraint(fields=('aluno', 'professor'), name='unique_recomendacao'),
        ),
        migrations.AddConstraint(
            model_name='uc_skills',
            constraint=models.UniqueConstraint(fields=('skills', 'uc'), name='unique_UC_Skills'),
        ),
    ]