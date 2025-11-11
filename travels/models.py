from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
# Eliminamos las importaciones de signals (pre_save, receiver) y la función generate_unique_slug

class TravelPost(models.Model):
    """
    Modelo para representar una publicación de viaje (post).
    Incluye un slug autogenerado para URLs amigables.
    """
    title = models.CharField(max_length=200, verbose_name="Título del Viaje")
    content = models.TextField(verbose_name="Relato de la Aventura")
    location = models.CharField(max_length=100, verbose_name="Ubicación Principal")
    image = models.ImageField(upload_to='travel_pics/', null=True, blank=True, verbose_name="Foto Principal")
    # Si no tienes este campo, bórralo, pero lo incluyo por robustez:
    image_caption = models.CharField(max_length=255, blank=True, verbose_name="Pie de foto") 
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Autor")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")
    
    # El campo crucial para las URLs amigables
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    class Meta:
        verbose_name = "Publicación de Viaje"
        verbose_name_plural = "Publicaciones de Viaje"
        ordering = ['-created_at']

    def __str__(self):
        """Retorna el título del post."""
        return self.title
    
    # -----------------------------------------------------
    # Sobrescribe save() para generar el slug de forma segura y única
    # -----------------------------------------------------
    def save(self, *args, **kwargs):
        # 1. Genera el slug solo si el slug está vacío.
        if not self.slug:
            self.slug = slugify(self.title)
            
            # 2. Asegura unicidad
            original_slug = self.slug
            num = 1
            # Itera mientras exista un post con este slug que NO sea la instancia actual
            while TravelPost.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f'{original_slug}-{num}'
                num += 1
                
        super().save(*args, **kwargs)

    # -----------------------------------------------------
    # MÉTODO CLAVE: Determina la URL canónica del objeto (para redirección)
    # -----------------------------------------------------
    def get_absolute_url(self):
        """
        Retorna la URL de detalle para este post usando su slug.
        """
        # Debe coincidir con el 'name' en travels/urls.py
        return reverse('travels:detail', kwargs={'slug': self.slug})
    