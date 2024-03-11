from django.db import models
from usuarios.models import Usuario

# Create your models here.
class Tarefa(models.Model):
    id_tarefa = models.AutoField(primary_key=True, editable=False)
    titulo = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255)
    data = models.DateField()
    hora = models.TimeField()
    finalizada = models.BooleanField(default=False)
    usuario_fk = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f'Instância: {self.id_tarefa}, Entidade: {self.__class__.__name__}'