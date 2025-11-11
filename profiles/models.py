from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from PIL import Image # NECESARIO: pip install Pillow

# Función para definir la ruta de subida de la imagen
def profile_image_upload_path(instance, filename):
    # La imagen se guardará en: media/profiles/user_<id>/<nombre_archivo>
    return f'profiles/user_{instance.user.id}/{filename}'

class Profile(models.Model):
    """
    Modelo de perfil que extiende la información del usuario de Django.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario")
    
    # Se renombra el campo a 'avatar' para estandarizar
    avatar = models.ImageField(
        default='profile_pics/default.jpg', # Imagen por defecto si no se sube ninguna
        upload_to=profile_image_upload_path,
        verbose_name="Foto de Perfil"
    )
    
    # Campo de biografía o descripción del viajero
    bio = models.TextField(max_length=500, blank=True, verbose_name="Biografía")
    
    # Campo para la fecha de nacimiento
    birth_date = models.DateField(null=True, blank=True, verbose_name="Fecha de Nacimiento")
    
    # Campo para la ubicación
    location = models.CharField(max_length=100, blank=True, verbose_name="Ubicación")

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return f'Perfil de {self.user.username}'
    
    def get_absolute_url(self):
        """Devuelve la URL canónica del objeto de perfil."""
        return reverse('profiles:detail', kwargs={'username': self.user.username})

    # Sobrescribimos el método save para redimensionar la imagen (opcional pero recomendado)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Solo redimensiona si se ha cargado una imagen y no es la por defecto
        # y si la imagen existe en el sistema de archivos (puede fallar al guardar sin archivo)
        if self.avatar and self.avatar.name != 'profile_pics/default.jpg':
            try:
                # Abrir la imagen en la ruta de guardado
                img = Image.open(self.avatar.path)
                
                # Definir el tamaño máximo deseado
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.avatar.path)
            except (FileNotFoundError, IOError) as e:
                # Manejar errores de archivo o imagen corrupta
                print(f"Error al procesar la imagen de perfil: {e}")

# --- Señales de Django ---

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crea un perfil automáticamente cuando se crea un nuevo usuario."""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Guarda el perfil cuando se guarda el usuario (asegurando que exista)."""
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        # En caso de que se haya creado un usuario pero la señal falló, lo crea aquí.
        Profile.objects.create(user=instance)