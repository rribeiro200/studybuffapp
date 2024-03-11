from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Usuario
from django.contrib import messages
from django.core.exceptions import ValidationError
from utils.logout import deslogar


# FORM LOGIN
def formulario_login(request):
    mensagens_sessao = messages.get_messages(request)

    return render(request, 'usuarios/login.html/', {'messages': mensagens_sessao})

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        usuario = Usuario.objects.filter(
            email=email, senha=senha
        )

        if usuario:
            dict_usuario_sessao = {
            'id': usuario[0].id_usuario,
            'nome_completo': usuario[0].nome_completo,
            'email': usuario[0].email,
            'senha': usuario[0].senha,
        }
            request.session['usuario'] = dict_usuario_sessao
            return redirect('tarefas:index')
        else:
            messages.error(request, 'Credenciais inválidas. Por favor, verifique seu e-mail e senha.')
            return redirect('usuarios:formulario_login')
        
    return redirect('usuarios:formulario_login')

def logout(request):
    deslogar(request)
    return redirect('tarefas:index')



# FORM CADASTRO
def formulario_cadastro(request):
    # Pega as mensagens da sessão daquele usuário
    mensagens_sessao = messages.get_messages(request)

    return render(request, 'usuarios/cadastre-se.html', {'messages': mensagens_sessao})

def cadastre_se(request):
    if request.method == 'POST':
        emails_da_base = Usuario.objects.all().filter(email=request.POST.get('email'))
        
        if emails_da_base.exists():
            messages.error(request, 'Erro: E-mail já está em uso!')
            return redirect('usuarios:formulario_cadastro')

        if request.POST.get('nome_completo') == '':
            messages.error(request, 'Preencha seu nome')
            return redirect('usuarios:formulario_cadastro')
        
        senha1 = request.POST.get('senha')
        senha2 = request.POST.get('confirmarSenha')
        if senha2 != senha1:
            messages.error(request, 'Erro: Senhas não coincidem')
            return redirect('usuarios:formulario_cadastro')

        novo_usuario = Usuario.objects.create(
            nome_completo=request.POST.get('nome_completo'),
            email=request.POST.get('email'),
            senha=request.POST.get('senha'),
        )
        
        if novo_usuario:
            messages.success(request, 'Cadastro realizado com sucesso! Faça login')
            return redirect('usuarios:formulario_login')
        
    return redirect('usuarios:formulario_login')