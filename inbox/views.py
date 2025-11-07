from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def inbox_list(request):
    """
    Vista de marcador de posición para la bandeja de entrada.
    """
    # Renderiza una plantilla simple que debemos crear en el siguiente paso
    return render(request, 'inbox/inbox_list.html')