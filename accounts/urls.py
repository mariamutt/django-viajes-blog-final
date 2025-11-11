from django.urls import path
from . import views

# Definimos el namespace de la aplicación
app_name = 'accounts'

urlpatterns = [
    # Mapea la vista de registro (signup)
    path('signup/', views.signup_view, name='signup'),
    
    # Mapea la vista de inicio de sesión (login)
    # Nota: usamos 'login' como name para que coincida con la plantilla
    path('login/', views.login_view, name='login'), 
    
    # Mapea la vista de cierre de sesión (logout)
    path('logout/', views.logout_view, name='logout'), 
    
    # Mapea la vista de perfil (profile)
    path('profile/', views.profile_view, name='profile'),
]