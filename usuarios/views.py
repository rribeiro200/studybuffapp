from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from .models import Usuario
from django.contrib import messages
from django.core.exceptions import ValidationError
from utils.logout import deslogar
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, FormView, View
from utils.valida_cadastro import valida_cadastro



# FORM LOGIN
class FormularioLoginView(TemplateView):
    template_name = 'usuarios/login.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx['messages'] = messages.get_messages(self.request)
        
        return ctx

class Login(FormView):
    template_name = 'usuarios/login.html'
    success_url = 'tarefas/index.html'

    def post(self, request, *args, **kwargs):
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
            nome_usuario_completo = request.session['usuario']['nome_completo']
            messages.success(request, f'Seja bem vindo {nome_usuario_completo}')

            return render(request, 'tarefas/index.html', {'nome': nome_usuario_completo})
        else:
            messages.error(request, 'Credenciais inválidas. Por favor, verifique seu e-mail e senha.')

            return redirect('usuarios:formulario_login')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    

class Logout(View):
    def get(self, request):
        deslogar(request)

        return redirect('tarefas:index')


# FORM CADASTRO
class FormularioCadastroView(TemplateView):
    template_name = 'usuarios/cadastre-se.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx['messages'] = messages.get_messages(self.request)
        return ctx


class CadastreSe(FormView):
    success_url = 'usuarios/login.html'
    template_name = 'usuarios/login.html'

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        dados_inputados = {
            'nome_completo': request.POST.get('nome_completo'), 
            'email': request.POST.get('email'),
            'senha': request.POST.get('senha'),
            'senha2': request.POST.get('confirmarSenha'),
        }
        if self.valida_cadastro(request, dados_inputados):
            novo_usuario = Usuario.objects.create(
                nome_completo=dados_inputados['nome_completo'],
                email=dados_inputados['email'],
                senha=dados_inputados['senha'],
                ativo=True
            )
            # Adiciona uma mensagem de sucesso e redireciona para a página de login
            messages.success(request, 'Cadastro realizado com sucesso! Faça login')
            return HttpResponseRedirect(reverse('usuarios:login'))
        else:
            return HttpResponseRedirect(reverse('usuarios:formulario_cadastro'))

    def valida_cadastro(self, request, dados_inputados):
        # Implemente a lógica de validação aqui
        if not dados_inputados['nome_completo']:
            messages.error(request, 'Preencha seu nome')
            return False
        
        if not dados_inputados['senha'] or dados_inputados['senha'] != dados_inputados['senha2']:
            messages.error(request, 'Erro: Senhas não coincidem')
            return False

        if Usuario.objects.filter(email=dados_inputados['email']).exists():
            messages.error(request, 'Erro: E-mail já está em uso!')
            return False
        
        return True

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return render(request, self.template_name)



def cadastre_se(request):
    if request.method == 'POST':
            

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