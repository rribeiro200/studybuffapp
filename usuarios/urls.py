from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    # LOGIN
    path('login/form/', views.formulario_login, name='formulario_login'),
    path('login/', views.login, name='login'),

    # LOGOUT
    path('logout/', views.logout, name='logout'),

    # CADASTRE-SE
    path('cadastro/form/', views.formulario_cadastro, name='formulario_cadastro'),
    path('cadastro/', views.cadastre_se, name='cadastro'),
]