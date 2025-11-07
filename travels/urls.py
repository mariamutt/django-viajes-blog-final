from django.urls import path
# Importación explícita de todas las clases de vistas desde .views
from .views import (
    TravelPostListView,
    TravelPostCreateView,
    TravelPostDetailView,
    TravelPostUpdateView,
    TravelPostDeleteView
)

# Usamos 'app_name' para poder referenciar las rutas como 'travels:list', 'travels:create', etc.
app_name = 'travels'

urlpatterns = [
    # R (Read) - Listado de posts
    # Ruta: /posts/
    # Usamos la clase importada directamente (sin 'views.')
    path('', TravelPostListView.as_view(), name='list'), 
    
    # C (Create) - Crear un nuevo post
    # Ruta: /posts/create/
    path('create/', TravelPostCreateView.as_view(), name='create'),
    
    # R (Read) - Detalle de un post (Usa el SLUG para URL amigable)
    # Ruta: /posts/<slug-del-post>/
    path('<slug:slug>/', TravelPostDetailView.as_view(), name='detail'),
    
    # U (Update) - Editar un post existente (Usa el SLUG)
    # Ruta: /posts/<slug-del-post>/edit/
    path('<slug:slug>/edit/', TravelPostUpdateView.as_view(), name='update'),
    
    # D (Delete) - Eliminar un post (Usa el SLUG)
    # Ruta: /posts/<slug-del-post>/delete/
    path('<slug:slug>/delete/', TravelPostDeleteView.as_view(), name='delete'),
]