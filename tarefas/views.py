from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Tarefa
from usuarios.models import Usuario
from django.contrib import messages

# Create your views here.
def index(request):
    mensagens = messages.get_messages(request)
    return render(request, 'tarefas/index.html', {'messages': mensagens})


def criar_tarefa(request):
    if request.method == "POST" and request.session['usuario'] is not None:
        id_usuario_sessao = request.session['usuario']['id']

        titulo_tarefa = request.POST.get('tituloTarefa')
        descricao_tarefa = request.POST.get('descricaoTarefa')
        data_tarefa = request.POST.get('dataTarefa')
        horario_tarefa = request.POST.get('horarioTarefa')

        usuario_tarefa = Usuario.objects.filter(id_usuario=id_usuario_sessao).first()
        
        if usuario_tarefa:
            if titulo_tarefa and data_tarefa is not None:
                nova_tarefa = Tarefa.objects.create(
                    titulo=titulo_tarefa,
                    descricao=descricao_tarefa,
                    data=data_tarefa,
                    hora=horario_tarefa,
                    usuario_fk=usuario_tarefa
                )
                if nova_tarefa.save:
                    messages.success(request, 'Tarefa criada com sucesso! Veja-a em "Minhas tarefas"')
                    return redirect('tarefas:index')
                
    return redirect('tarefas:index')


def minhas_tarefas(request):
    id_usuario_sessao = request.session['usuario']['id']
    usuario_tarefa = Usuario.objects.filter(id_usuario=id_usuario_sessao).first()
    tarefas_do_usuario = Tarefa.objects.all().filter(usuario_fk=usuario_tarefa)
    
    if tarefas_do_usuario:
        return render(request, 'tarefas/minhas_tarefas.html', {'tarefas': tarefas_do_usuario})
    else:
        return render(request, 'tarefas/minhas_tarefas.html')
