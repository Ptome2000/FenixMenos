# Generated by Django 5.0.4 on 2024-05-01 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Community', '0002_categoria_logo_comentario_imagem_post_imagem'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoria',
            name='postagens',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='comentarios',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='categoria',
            name='logo',
            field=models.ImageField(upload_to='Categorias'),
        ),
    ]
