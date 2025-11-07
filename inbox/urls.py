from django.urls import path
from . import views

# Definimos el namespace 'inbox'
app_name = 'inbox'

urlpatterns = [
    # La ruta raíz de la aplicación /inbox/
    # El nombre 'list' debe coincidir con el 'inbox:list' usado en base.html
    path('', views.inbox_list, name='list'),
]