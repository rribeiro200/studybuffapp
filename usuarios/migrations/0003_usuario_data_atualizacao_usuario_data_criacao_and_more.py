# Generated by Django 5.0.3 on 2024-03-18 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_usuario_ativo'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='data_atualizacao',
            field=models.DateTimeField(default=None),
        ),
        migrations.AddField(
            model_name='usuario',
            name='data_criacao',
            field=models.DateTimeField(default=None),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='ativo',
            field=models.BooleanField(),
        ),
    ]