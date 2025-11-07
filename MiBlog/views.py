from django.shortcuts import render

# Vista principal para la página de inicio (Home)
def home(request):
    """
    Renderiza la página de inicio. Esta función utiliza 'render' para
    procesar la plantilla 'home.html' y no devuelve texto plano.
    """
    return render(request, 'home.html')

# Vista para la página Acerca de Mí (About)
def about(request):
    """
    Renderiza la página 'Acerca de Mí'.
    """
    return render(request, 'about.html')