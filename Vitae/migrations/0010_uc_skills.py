# Generated by Django 5.0.4 on 2024-05-11 18:44

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vitae', '0009_remove_uc_skills'),
    ]

    operations = [
        migrations.CreateModel(
            name='UC_Skills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nivel', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('skills', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Vitae.skills')),
                ('uc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Vitae.uc')),
            ],
        ),
    ]
