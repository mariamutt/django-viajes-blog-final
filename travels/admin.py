from django.contrib import admin
from .models import TravelPost

# Usamos el decorador para registrar el modelo TravelPost
@admin.register(TravelPost)
class TravelPostAdmin(admin.ModelAdmin):
    # Esto le dice al administrador que automáticamente genere el campo 'slug'
    # usando el contenido del campo 'title' mientras escribes.
    prepopulated_fields = {'slug': ('title',)}
    
    # Define qué columnas se muestran en la página de listado del administrador.
    list_display = ('title', 'author', 'created_at')
    
    # Permite filtrar los posts por 'author' y 'created_at'.
    list_filter = ('author', 'created_at')
    
    # Agrega una caja de búsqueda para buscar por título y contenido.
    search_fields = ('title', 'content')
