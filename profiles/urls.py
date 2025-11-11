from django.urls import path
from . import views

# Define el nombre de la aplicación para evitar conflictos de nombres
app_name = 'profiles' 

urlpatterns = [
    # 1. Listado de perfiles (opcional) - Mapea a /profiles/
    path('', views.profile_list, name='list'),
    
    # 2. Perfil del usuario autenticado (Redirecciona al detalle) - Mapea a /profiles/me/
    path('me/', views.my_profile_view, name='my_profile'),
    
    # 3. Ruta de edición de perfil - Mapea a /profiles/editar/
    path('editar/', views.profile_edit, name='edit'),

    # 4. Detalle de perfil por nombre de usuario (DEBE IR AL FINAL) - Mapea a /profiles/<username>/
    path('<str:username>/', views.profile_detail, name='detail'), 
]