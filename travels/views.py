from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import TravelPost
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied


# --- Mixin de Seguridad ---

class AuthorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Asegura que el usuario esté logeado (LoginRequiredMixin)
    y que solo el autor pueda editar o borrar (UserPassesTestMixin).
    """
    def test_func(self):
        # Obtiene el objeto (post) actual que se está intentando manipular
        post = self.get_object()
        # Devuelve True si el usuario actual es el autor del post
        return self.request.user == post.author

    def handle_no_permission(self):
        # Si la prueba falla, eleva un error de Permiso Denegado
        if self.request.user.is_authenticated:
            raise PermissionDenied("No tienes permiso para modificar este post.")
        # Si no está autenticado, simplemente redirige al login
        return super().handle_no_permission()


# --- Vistas CRUD ---

class TravelPostListView(ListView):
    """Muestra una lista de todos los posts de viaje."""
    model = TravelPost
    template_name = 'travels/travel_post_list.html'
    context_object_name = 'posts'
    ordering = ['-date_posted'] # Ordenar por fecha de publicación descendente (más reciente primero)
    paginate_by = 10 # Paginación (opcional)


class TravelPostDetailView(DetailView):
    """Muestra los detalles de un post específico usando el SLUG."""
    model = TravelPost
    template_name = 'travels/travel_post_detail.html'
    context_object_name = 'post'
    # Utiliza 'slug' en lugar de 'pk' para buscar el post en la URL


class TravelPostCreateView(LoginRequiredMixin, CreateView):
    """Permite a los usuarios autenticados crear un nuevo post."""
    model = TravelPost
    template_name = 'travels/travel_post_form.html'
    # Los campos que se mostrarán en el formulario
    fields = ['title', 'content', 'destination', 'image'] 

    def form_valid(self, form):
        """Asigna automáticamente el autor antes de guardar."""
        form.instance.author = self.request.user
        return super().form_valid(form)


class TravelPostUpdateView(AuthorRequiredMixin, UpdateView):
    """Permite al autor editar su propio post."""
    model = TravelPost
    template_name = 'travels/travel_post_form.html'
    fields = ['title', 'content', 'destination', 'image']


class TravelPostDeleteView(AuthorRequiredMixin, DeleteView):
    """Permite al autor eliminar su propio post."""
    model = TravelPost
    template_name = 'travels/travel_post_confirm_delete.html'
    # Redirige a la lista de posts después de la eliminación
    success_url = reverse_lazy('travels:list')