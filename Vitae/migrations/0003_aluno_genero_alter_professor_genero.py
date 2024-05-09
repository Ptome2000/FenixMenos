# Generated by Django 5.0.4 on 2024-05-09 21:06

import Vitae.models
import django_enumfield.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Vitae', '0002_alter_aluno_foto'),
    ]

    operations = [
        migrations.AddField(
            model_name='aluno',
            name='genero',
            field=django_enumfield.db.fields.EnumField(default=0, enum=Vitae.models.Genero),
        ),
        migrations.AlterField(
            model_name='professor',
            name='genero',
            field=django_enumfield.db.fields.EnumField(default=0, enum=Vitae.models.Genero),
        ),
    ]
