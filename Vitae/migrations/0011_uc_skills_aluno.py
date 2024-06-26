# Generated by Django 5.0.4 on 2024-05-11 18:45

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vitae', '0010_uc_skills'),
    ]

    operations = [
        migrations.CreateModel(
            name='UC_Skills_Aluno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progresso', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('alunOo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Vitae.aluno')),
                ('uc_skills', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Vitae.uc_skills')),
            ],
        ),
    ]
