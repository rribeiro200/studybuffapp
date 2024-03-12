from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Tarefa
from usuarios.models import Usuario
from django.contrib import messages

# Create your views here.
def index(request):
    mensagens = messages.get_messages(request)

    # Renderiza o index mesmo se a sessão estiver vazia
    if not 'usuario' in request.session:
        return render(request, 'tarefas/index.html', {'messages': mensagens})
    else:
        # Se tiver usuário na sessão, renderiza as tarefas dele no carrousel
        id_usuario_sessao = request.session['usuario']['id']
        usuario_tarefa = Usuario.objects.filter(id_usuario=id_usuario_sessao).first()
        tarefas_do_usuario = Tarefa.objects.all().filter(usuario_fk=usuario_tarefa, finalizada=False)
        return render(request, 'tarefas/index.html', {'messages': mensagens, 'tarefas': tarefas_do_usuario})



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

                if nova_tarefa:
                    messages.success(request, f'"{titulo_tarefa}" criada!')
                    return redirect('tarefas:minhas_tarefas')
                
    return redirect('tarefas:minhas_tarefas')


def minhas_tarefas(request):
    id_usuario_sessao = request.session['usuario']['id']
    usuario_tarefa = Usuario.objects.filter(id_usuario=id_usuario_sessao).first()

    tarefas_do_usuario = Tarefa.objects.all().filter(usuario_fk=usuario_tarefa)
    tarefas_concluidas = Tarefa.objects.filter(usuario_fk=usuario_tarefa, finalizada=True)
    tarefas_em_andamento = Tarefa.objects.filter(usuario_fk=usuario_tarefa, finalizada=False)
    
    if tarefas_do_usuario:
        return render(request, 'tarefas/minhas_tarefas.html', {'tarefas': tarefas_do_usuario, 'tarefas_concluidas': tarefas_concluidas, 'tarefas_em_andamento': tarefas_em_andamento})
    else:
        return render(request, 'tarefas/minhas_tarefas.html')


def editar_tarefa(request, pk):
    tarefa = Tarefa.objects.filter(pk=pk).first()

    if request.method == 'POST':    
        novo_titulo = request.POST.get('titulo')
        nova_descricao = request.POST.get('descricao')
        nova_data = request.POST.get('data')
        nova_hora = request.POST.get('hora')
        finalizada = request.POST.get('finalizada') # Retorna TRUE ou FALSE <option value="">

        # Validar campos
        if not novo_titulo:
            messages.error(request, 'O título é obrigatório.')
            return redirect('tarefas:editar_tarefa', pk=pk)
        elif not nova_descricao:
            messages.error(request, 'A descrição é obrigatória.')
            return redirect('tarefas:editar_tarefa', pk=pk)
        elif not nova_data:
            messages.error(request, 'A data é obrigatória.')
            return redirect('tarefas:editar_tarefa', pk=pk)
        elif not nova_hora:
            messages.error(request, 'A hora é obrigatória.')
            return redirect('tarefas:editar_tarefa', pk=pk)
        else:
            # Atualizar a tarefa
            tarefa_atualizada = Tarefa.objects.filter(pk=pk).update(
                titulo=novo_titulo,
                descricao=nova_descricao,
                data=nova_data,
                hora=nova_hora,
                finalizada=finalizada
            )

            if tarefa_atualizada:
                messages.info(request, f'"{novo_titulo}" atualizada com sucesso!')
                return redirect('tarefas:minhas_tarefas')
    
        tarefas_do_usuario = Tarefa.objects.filter(usuario_fk=request.session['usuario']['id'])
        
        return render(request, 'tarefas/minhas_tarefas.html', {'tarefas': tarefas_do_usuario})

    return render(request, 'tarefas/editar_tarefa.html', {'tarefa': tarefa})


def excluir_tarefa(request, pk):
    tarefa = Tarefa.objects.filter(pk=pk).first()

    if tarefa:
        tarefa.delete()
        messages.error(request, f'{tarefa.titulo} deletada!')
        return redirect('tarefas:minhas_tarefas')

    return redirect('tarefas:minhas_tarefas')


def finalizar_tarefa(request, pk):
    tarefa = Tarefa.objects.filter(pk=pk).first()

    if tarefa.finalizada == 0: # Se for False
        tarefa.finalizada = 1 # Recebe True
        tarefa.save()
        messages.success(request, f'Parabéns por finalizar sua tarefa: "{tarefa.titulo}"')
        
        return redirect('tarefas:minhas_tarefas')

    return redirect('tarefas:minhas_tarefas')