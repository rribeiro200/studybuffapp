def deslogar(request):
    if request.session['usuario']:
        del request.session['usuario']