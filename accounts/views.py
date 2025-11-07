from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm 
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

# 1. Vista de Registro (Signup)
def signup(request):
    """
    Maneja la lógica de registro de nuevos usuarios.
    """
    if request.method == 'POST':
        # Instancia el formulario con los datos recibidos
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Guarda el nuevo usuario
            form.save()
            username = form.cleaned_data.get('username')
            # Envía un mensaje de éxito al usuario
            messages.success(request, f'¡Cuenta creada exitosamente para {username}! Ya puedes iniciar sesión.')
            # Redirige a la página de login (la URL 'login' está definida por django.contrib.auth.urls)
            return redirect('login') 
    else:
        # Crea un formulario vacío si es una petición GET
        form = UserCreationForm()
        
    # Renderiza la plantilla de registro
    return render(request, 'registration/signup.html', {'form': form})

# 2. Vista de Perfil
@login_required 
def profile(request):
    """
    Renderiza la página de perfil del usuario.
    """
    # Renderiza la plantilla de perfil, pasando el objeto 'user' que ya está en el contexto
    return render(request, 'accounts/profile.html')

# 3. Personalización del Login (opcional, incluido por completitud)
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    
    def get_success_url(self):
        # Redirigir al inicio después de un login exitoso y usar el sistema de mensajes
        messages.success(self.request, f'¡Bienvenido de nuevo, {self.request.user.username}!')
        return reverse_lazy('home')