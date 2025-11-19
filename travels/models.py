from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class TravelPost(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título")
    subtitle = models.CharField(max_length=255, verbose_name="Subtítulo", blank=True)
    content = RichTextField(verbose_name="Contenido") # Requiere ckeditor
    image = models.ImageField(upload_to='travel_images/', verbose_name="Imagen Principal")
    created_at = models.DateField(auto_now_add=True, verbose_name="Fecha de Publicación")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']