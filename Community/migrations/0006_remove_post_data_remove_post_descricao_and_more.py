# Generated by Django 5.0.4 on 2024-05-04 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Community', '0005_remove_categoria_postagens_remove_post_comentarios_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='data',
        ),
        migrations.RemoveField(
            model_name='post',
            name='descricao',
        ),
        migrations.RemoveField(
            model_name='post',
            name='imagem',
        ),
        migrations.AlterField(
            model_name='categoria',
            name='designacao',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]