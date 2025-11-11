from django.urls import path
from .views import (
    TravelPostListView, 
    TravelPostDetailView, 
    TravelPostCreateView, 
    TravelPostUpdateView, 
    TravelPostDeleteView,
    user_post_list_view 
)

app_name = 'travels'

urlpatterns = [
    # 1. Rutas Fijas / Específicas
    # DEBEN ir antes que la ruta de detalle con slug.
    
    # 1.1 CREAR (Ruta /travels/create/)
    path('create/', TravelPostCreateView.as_view(), name='create'),
    
    # 1.2 POSTS DE USUARIO (Ruta /travels/usuario/1/posts/)
    path('usuario/<int:user_id>/posts/', user_post_list_view, name='user_posts'),

    # --------------------------------------------------------------------------------
    # 2. Rutas Basadas en Slug (Acepta cualquier string, debe ir al final de las fijas)

    # 2.1 DETALLE (Ruta /travels/mi-titulo-de-post/) - AHORA COINCIDE CORRECTAMENTE
    path('<slug:slug>/', TravelPostDetailView.as_view(), name='detail'),
    
    # 2.2 ACTUALIZAR (Ruta /travels/mi-titulo-de-post/update/)
    path('<slug:slug>/update/', TravelPostUpdateView.as_view(), name='edit'), 
    
    # 2.3 BORRAR (Ruta /travels/mi-titulo-de-post/delete/)
    path('<slug:slug>/delete/', TravelPostDeleteView.as_view(), name='delete'),

    # 3. LISTADO GENERAL (Ruta /travels/) - Se deja al final o al inicio, ya que no tiene argumentos
    path('', TravelPostListView.as_view(), name='list'), 
]