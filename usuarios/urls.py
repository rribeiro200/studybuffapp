from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    # LOGIN
    path('login/form/', views.FormularioLoginView.as_view(), name='formulario_login'),
    path('login/', views.Login.as_view(), name='login'),

    # LOGOUT
    path('logout/', views.Logout.as_view(), name='logout'),

    # CADASTRE-SE
    path('cadastro/form/', views.FormularioCadastroView.as_view(), name='formulario_cadastro'),
    path('cadastro/', views.CadastreSe.as_view(), name='cadastro'),
]