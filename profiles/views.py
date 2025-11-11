from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile 
from .forms import ProfileUpdateForm 
from travels.models import TravelPost # Necesario para listar posts

# --- VISTA 1: Perfil del Usuario Autenticado (Redirige al detalle) ---
@login_required 
def my_profile_view(request):
    """
    Redirige al perfil detallado del usuario actual.
    Esta es la vista que se usa con el nombre 'my_profile' en profiles/urls.py
    """
    return redirect('profiles:detail', username=request.user.username)


# --- VISTA 2: Listado de Perfiles ---
def profile_list(request):
    """Muestra una lista de todos los usuarios/perfiles."""
    users = User.objects.all().order_by('username').select_related('profile') 
    context = {
        'users': users,
        'page_title': 'Explorar Viajeros'
    }
    return render(request, 'profiles/profile_list.html', context)


# --- VISTA 3: Detalle de Perfil por Username ---
def profile_detail(request, username):
    """Muestra el detalle del perfil de un usuario específico por su nombre de usuario."""
    user = get_object_or_404(User, username=username)
    
    # Intenta acceder directamente al perfil (asumiendo que la señal lo creó)
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        # En caso de error, creamos el perfil como medida defensiva
        profile = Profile.objects.create(user=user)

    # Verifica si el usuario actual está viendo su propio perfil
    is_current_user = request.user.is_authenticated and request.user == user

    # Filtramos los posts del usuario objetivo
    recent_posts = TravelPost.objects.filter(author=user).order_by('-created_at')[:3]

    context = {
        'target_user': user, # El usuario cuyo perfil estamos viendo
        'profile': profile,
        'recent_posts': recent_posts,
        'is_current_user': is_current_user, # Para mostrar el botón de Editar/Seguir
        'page_title': f'Perfil de {username}'
    }
    return render(request, 'profiles/profile_detail.html', context)


# --- VISTA 4: Editar Perfil ---
@login_required
def profile_edit(request):
    """Permite al usuario autenticado editar su propio perfil."""
    profile_instance = request.user.profile 

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile_instance)
        
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tu perfil ha sido actualizado exitosamente!')
            return redirect('profiles:detail', username=request.user.username)
        else:
            messages.error(request, 'Hubo un error al guardar tu perfil. Por favor, revisa los campos.')
    else:
        form = ProfileUpdateForm(instance=profile_instance)

    context = {
        'form': form,
        'page_title': 'Editar Perfil'
    }
    return render(request, 'profiles/profile_form.html', context)
