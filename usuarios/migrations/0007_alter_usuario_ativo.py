# Generated by Django 5.0.3 on 2024-03-18 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0006_alter_usuario_data_atualizacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='ativo',
            field=models.BooleanField(null=True),
        ),
    ]
