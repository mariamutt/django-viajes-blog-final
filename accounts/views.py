from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

# Vista para el Registro de Usuarios (Signup)
def signup_view(request):
    if request.method == 'POST':
        # Instancia el formulario con los datos del POST
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Guarda el nuevo usuario
            user = form.save()
            # Inicia sesión automáticamente con el nuevo usuario
            login(request, user)
            messages.success(request, f"¡Bienvenido, {user.username}! Tu cuenta ha sido creada.")
            # Redirige a la página principal o donde sea apropiado
            return redirect('/') 
        else:
            # Si el formulario no es válido, muestra errores.
            messages.error(request, "Error al crear la cuenta. Por favor, revisa el formulario.")
    else:
        # Si es una solicitud GET, muestra el formulario vacío
        form = UserCreationForm()
    
    # Renderiza la plantilla con el formulario
    return render(request, 'accounts/signup.html', {'form': form})


# Vista para el Inicio de Sesión (Login)
def login_view(request):
    if request.method == 'POST':
        # Instancia el formulario de autenticación con los datos del POST
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Autentica al usuario
            user = form.get_user()
            # Inicia sesión
            login(request, user)
            messages.success(request, f"¡Has iniciado sesión como {user.username}!")
            
            # Revisa si hay un parámetro 'next' en la URL (para redirigir después del login)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                # Si no hay 'next', redirige a la página principal
                return redirect('/')
        else:
            # Si el formulario no es válido
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")
    else:
        # Si es una solicitud GET, muestra el formulario vacío
        form = AuthenticationForm()
        
    return render(request, 'accounts/login.html', {'form': form})


# Vista para el Cierre de Sesión (Logout)
# No necesita un formulario, solo la acción
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('/')


# Vista de Perfil (requiere que el usuario esté logeado)
@login_required 
def profile_view(request):
    # Ya sabemos que el usuario está logeado gracias al decorador @login_required
    return render(request, 'accounts/profile.html')