from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse

# Definición del Modelo TravelPost
class TravelPost(models.Model):
    # Campo de Título, no puede estar vacío
    title = models.CharField(max_length=200, verbose_name="Título del Post")
    
    # Contenido completo del post
    content = models.TextField(verbose_name="Relato de la Aventura")
    
    # Relación uno a muchos con el modelo User de Django.
    # CASCADE: Si se borra el usuario, se borran todos sus posts.
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Destino del viaje
    destination = models.CharField(max_length=100, verbose_name="Destino")
    
    # Fecha de publicación, se establece automáticamente al crearse el post
    date_posted = models.DateTimeField(auto_now_add=True)
    
    # Campo para la imagen, se almacena en 'media/travel_images/'
    # Blank=True: El campo no es obligatorio en el formulario.
    image = models.ImageField(upload_to='travel_images/', blank=True, null=True, verbose_name="Imagen Principal")
    
    # SLUG: Campo único y amigable para las URL, se genera automáticamente.
    slug = models.SlugField(unique=True, max_length=255, editable=False)
    
    class Meta:
        # Nombre singular y plural que se mostrará en el administrador de Django
        verbose_name = "Post de Viaje"
        verbose_name_plural = "Posts de Viaje"
        # Ordenación por defecto (más nuevo primero)
        ordering = ['-date_posted']

    def __str__(self):
        """Devuelve el título del post para una mejor representación."""
        return self.title

    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para generar automáticamente el slug 
        a partir del título antes de guardar el objeto.
        """
        if not self.slug:
            # Crea un slug a partir del título
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Define la URL a la que el usuario es redirigido después de crear/editar un post.
        Redirige a la vista de detalle del post recién creado/editado.
        """
        return reverse('travels:detail', kwargs={'slug': self.slug})