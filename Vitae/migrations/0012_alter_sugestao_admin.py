# Generated by Django 5.0.5 on 2024-05-11 22:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vitae', '0011_uc_skills_aluno'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='sugestao',
            name='admin',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='avaliado_por', to=settings.AUTH_USER_MODEL),
        ),
    ]
