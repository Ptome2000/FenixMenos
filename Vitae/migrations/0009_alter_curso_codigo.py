# Generated by Django 5.0.4 on 2024-05-10 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vitae', '0008_alter_curso_codificado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curso',
            name='codigo',
            field=models.IntegerField(max_length=4, primary_key=True, serialize=False),
        ),
    ]
