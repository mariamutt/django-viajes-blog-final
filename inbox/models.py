from django.db import models
from django.conf import settings 
from django.utils import timezone

# Nota: settings.AUTH_USER_MODEL apunta al modelo de Usuario que estés usando.

class Message(models.Model):
    """
    Representa un mensaje privado entre dos usuarios (la estructura más sencilla).
    """
    
    # Remitente (el usuario que envía el mensaje)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, # Referencia estándar al modelo User
        related_name='sent_messages', 
        on_delete=models.SET_NULL, # Si el remitente es eliminado, el mensaje permanece
        null=True, # Permitir valor nulo si el remitente se borra
        verbose_name='Remitente'
    )
    
    # Destinatario (el usuario que recibe el mensaje)
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, # Referencia estándar al modelo User
        related_name='received_messages', 
        on_delete=models.CASCADE, # Si el destinatario es eliminado, el mensaje se elimina
        verbose_name='Destinatario'
    )
    
    # Contenido del mensaje
    content = models.TextField(verbose_name='Contenido del Mensaje')
    
    # Marca de tiempo de cuándo se envió el mensaje
    timestamp = models.DateTimeField(
        default=timezone.now, # Usamos timezone.now para consistencia
        verbose_name='Fecha de Envío'
    )
    
    # Campo booleano para rastrear si el mensaje ha sido leído por el destinatario
    is_read = models.BooleanField(
        default=False, 
        verbose_name='Leído'
    )

    class Meta:
        # Ordenamos los mensajes por la marca de tiempo, los más nuevos primero
        ordering = ['-timestamp'] 
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'

    def __str__(self):
        # Representación legible del mensaje en el Admin
        # Usamos el ternario para manejar el caso de un sender=None
        sender_username = self.sender.username if self.sender else 'Usuario Eliminado'
        return f"De: {sender_username} a: {self.receiver.username} - ({self.timestamp.strftime('%Y-%m-%d %H:%M')})"