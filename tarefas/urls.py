from django.urls import path
from . import views

app_name = 'tarefas'

urlpatterns = [
    # Página principal
    path('', views.index, name='index'),

    # CRUD
    path('tarefa/criar/', views.criar_tarefa, name='criar_tarefa'),
    path('minhas_tarefas/', views.minhas_tarefas, name='minhas_tarefas'),
    path('editar_tarefa/<int:pk>', views.editar_tarefa, name='editar_tarefa'),
]
