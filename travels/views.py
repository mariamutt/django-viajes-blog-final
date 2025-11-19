from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
from .models import TravelPost
from .forms import PostForm  # <--- ¡AQUÍ ESTABA EL ERROR! Ahora coincide.

# Listado
class PostListView(ListView):
    model = TravelPost
    template_name = 'travels/travelpost_list.html' # Asegúrate que el template se llame así
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return TravelPost.objects.filter(
                Q(title__icontains=query) | Q(subtitle__icontains=query)
            ).order_by('-created_at')
        return TravelPost.objects.all().order_by('-created_at')

# Detalle
class PostDetailView(DetailView):
    model = TravelPost
    template_name = 'travels/post_detail.html'
    context_object_name = 'post'

# Creación
class PostCreateView(LoginRequiredMixin, CreateView):
    model = TravelPost
    form_class = PostForm
    template_name = 'travels/post_form.html'
    success_url = reverse_lazy('travels:list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# Edición
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = TravelPost
    form_class = PostForm
    template_name = 'travels/post_form.html'
    
    def get_success_url(self):
        return reverse_lazy('travels:detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Borrado
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = TravelPost
    template_name = 'travels/post_confirm_delete.html'
    success_url = reverse_lazy('travels:list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author