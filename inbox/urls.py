from django.urls import path
from . import views

urlpatterns = [
    # Muestra la lista de conversaciones únicas 
    path('', views.inbox_list, name='list'), 
    
    # Muestra los mensajes de una conversación específica, usando el ID del OTRO usuario.
    path('<int:user_id>/', views.inbox_detail, name='detail'), 

    # Permite iniciar un nuevo hilo de mensaje
    path('new/', views.inbox_new_thread, name='new_thread'),
]