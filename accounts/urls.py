from django.urls import path
from . import views

# Definimos el nombre de la aplicación para evitar colisiones
app_name = 'accounts' 

urlpatterns = [
    # Ruta de Registro (signup). Por ahora, apunta a la función views.signup
    path('signup/', views.signup, name='signup'),
    
    # Ruta de Perfil (profile). 
    path('profile/', views.profile, name='profile'),
]