# Generated by Django 5.0.4 on 2024-05-10 21:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vitae', '0005_alter_matricula_ano_alter_uc_acronimo_equipadocente_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uc',
            name='coordenador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Vitae.professor'),
        ),
    ]
