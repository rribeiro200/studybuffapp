from typing import Iterable
from django.db import models

# Create your models here.
class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True, editable=False)
    nome_completo = models.CharField(max_length=255)
    email = models.EmailField()
    senha = models.CharField(max_length=255)
    ativo = models.BooleanField(null=True)
    data_criacao = models.DateTimeField(auto_now_add=True) # automatico quando for criado
    data_atualizacao = models.DateTimeField(auto_now=True) # Automatico quando atualizado

    def __str__(self):
        return f'Instância: {self.id_usuario}, Entidade: {self.__class__.__name__}'