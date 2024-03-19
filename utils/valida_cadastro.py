from django.shortcuts import redirect
from usuarios.models import Usuario
from django.contrib import messages

def clean_email(request, dados_inputados):
    emails_da_base = Usuario.objects.all().filter(email=dados_inputados['email'])

    if emails_da_base.exists():
        messages.error(request, 'Erro: E-mail já está em uso!')
        return redirect('usuarios:formulario_cadastro')

def clean_nome_completo(request, dados_inputados):
    if dados_inputados['nome_completo'] == '':
        messages.error(request, 'Preencha seu nome')
        return redirect('usuarios:formulario_cadastro')         
    return dados_inputados['nome_completo']

def clean_senha(request, dados_inputados):
    if dados_inputados['senha'] != dados_inputados['senha2']:
        messages.error(request, 'Erro: Senhas não coincidem')
        return redirect('usuarios:formulario_cadastro')
    return dados_inputados['senha']

def valida_cadastro(request, dados_inputados):
    clean_email(request, dados_inputados)
    nome = clean_nome_completo(request, dados_inputados)
    senha = clean_senha(request, dados_inputados)

    novo_usuario = Usuario.objects.create(
        nome_completo=nome,
        email=dados_inputados['email'],
        senha=senha,
    )
    novo_usuario.save()

    return True