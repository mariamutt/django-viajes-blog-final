from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView
)
from .models import TravelPost 

# --- VISTAS BASADAS EN CLASES (CBVs) ---

class TravelPostListView(ListView):
    """Muestra una lista de todos los posts de viajes."""
    model = TravelPost
    # CORRECCIÓN CLAVE: Aseguramos que apunte al archivo que creaste
    template_name = 'travels/travelpost_list.html' 
    context_object_name = 'posts'
    ordering = ['-created_at'] 
    paginate_by = 10

class TravelPostDetailView(DetailView):
    """Muestra el detalle de un post individual usando el slug."""
    model = TravelPost
    template_name = 'travels/post_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

class TravelPostCreateView(LoginRequiredMixin, CreateView):
    """Permite a un usuario autenticado crear un nuevo post."""
    model = TravelPost
    fields = ['title', 'content', 'location', 'image'] 
    template_name = 'travels/post_form.html'

    def form_valid(self, form):
        # Asigna automáticamente el usuario que está logueado como autor
        form.instance.author = self.request.user
        return super().form_valid(form)

class TravelPostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Permite al autor de un post actualizarlo."""
    model = TravelPost
    fields = ['title', 'content', 'location', 'image']
    template_name = 'travels/post_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def test_func(self):
        # Verifica que solo el autor pueda editar el post
        post = self.get_object()
        return self.request.user == post.author

class TravelPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Permite al autor de un post eliminarlo."""
    model = TravelPost
    template_name = 'travels/post_confirm_delete.html' 
    success_url = '/travels/' # Redirige a la lista general después de borrar
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def test_func(self):
        # Verifica que solo el autor pueda eliminar el post
        post = self.get_object()
        return self.request.user == post.author

# --- VISTA BASADA EN FUNCIÓN PARA LISTAR POSTS POR USUARIO ---

def user_post_list_view(request, user_id):
    """
    Función requerida por el patrón de URL 'travels:user_posts'.
    Lista todos los posts creados por el usuario con el ID proporcionado.
    """
    
    target_user = get_object_or_404(User, id=user_id)

    # Filtramos por el modelo TravelPost
    user_posts = TravelPost.objects.filter(author=target_user).order_by('-created_at')

    context = {
        'target_user': target_user,
        'posts': user_posts,
        'page_title': f'Posts de {target_user.username}',
    }

    # Asegúrate de que esta plantilla exista
    return render(request, 'travels/user_posts_list.html', context)