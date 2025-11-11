from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q 
from django.contrib.auth import get_user_model 
from django.contrib import messages # Importamos el framework de mensajes para notificaciones
from .models import Message 

User = get_user_model() # Función estándar para obtener el modelo de usuario

@login_required
def inbox_list(request):
    """
    Muestra la lista de conversaciones únicas (bandeja de entrada).
    La lógica se basa en el último mensaje de cada par de usuarios.
    """
    # 1. Obtenemos todos los mensajes donde el usuario actual es remitente O destinatario.
    messages_query = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).order_by('-timestamp')

    # 2. Inicializamos estructuras para encontrar conversaciones únicas.
    participants = [] # Almacena IDs de usuarios únicos con los que se ha hablado
    last_messages = [] # Almacena el último mensaje de cada conversación única

    for message in messages_query:
        # Identificamos al otro participante de la conversación.
        if message.sender == request.user:
            other_user = message.receiver
        else:
            other_user = message.sender
        
        # Si el otro usuario no ha sido procesado, lo añadimos como una nueva conversación.
        if other_user and other_user.id not in participants:
            participants.append(other_user.id)
            last_messages.append(message)
    
    context = {
        'conversations': last_messages 
    }
    
    # La vista renderizará 'inbox/inbox_list.html'
    return render(request, 'inbox/inbox_list.html', context)

@login_required
def inbox_detail(request, user_id):
    """
    Muestra el detalle de la conversación con un usuario específico y permite responder.
    """
    # Obtenemos al otro usuario con el que se está conversando.
    other_user = get_object_or_404(User, id=user_id)
    
    # --- Lógica de envío de mensaje (POST) ---
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            # Creamos y guardamos el nuevo mensaje
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                content=content,
                is_read=False 
            )
            # Redirigimos al mismo hilo para ver el nuevo mensaje
            return redirect('inbox:detail', user_id=other_user.id)
        else:
            messages.error(request, 'El mensaje no puede estar vacío.')

    # --- Lógica de visualización (GET) ---

    # Obtenemos todos los mensajes entre el usuario actual (A) y el 'otro' usuario (B).
    # Filtramos donde A->B O B->A.
    messages_thread = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) | 
        Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')
    
    # Marcamos como leídos todos los mensajes recibidos no leídos de este hilo.
    Message.objects.filter(
        receiver=request.user, 
        sender=other_user, 
        is_read=False
    ).update(is_read=True)

    context = {
        'other_user': other_user,
        'messages': messages_thread,
    }
    # La vista renderizará 'inbox/inbox_detail.html'
    return render(request, 'inbox/inbox_detail.html', context)

@login_required
def inbox_new_thread(request):
    """
    Vista para crear un nuevo mensaje/hilo, buscando al destinatario por username.
    """
    if request.method == 'POST':
        receiver_username = request.POST.get('receiver_username')
        content = request.POST.get('content')

        if not receiver_username or not content:
            messages.error(request, 'Debes completar el nombre de usuario y el mensaje.')
            # Importante: redirigir de vuelta para mostrar el error
            return redirect('inbox:new_thread') 

        try:
            # Buscamos al usuario destinatario por el nombre de usuario
            receiver_user = User.objects.get(username=receiver_username)
        except User.DoesNotExist:
            messages.error(request, f'No se encontró ningún usuario con el nombre "{receiver_username}".')
            return redirect('inbox:new_thread')

        # Evitar enviarse mensajes a sí mismo
        if receiver_user == request.user:
            messages.warning(request, 'No puedes enviarte mensajes a ti mismo.')
            return redirect('inbox:new_thread')
            
        # Creamos el primer mensaje del nuevo hilo
        Message.objects.create(
            sender=request.user,
            receiver=receiver_user,
            content=content,
            is_read=False
        )

        # Redirigimos al usuario al hilo de conversación recién creado
        messages.success(request, f'Mensaje enviado a {receiver_user.username} exitosamente.')
        return redirect('inbox:detail', user_id=receiver_user.id)
    
    # Para la solicitud GET, simplemente renderizamos la plantilla de formulario.
    # La vista renderizará 'inbox/inbox_new_thread.html'
    return render(request, 'inbox/inbox_new_thread.html')