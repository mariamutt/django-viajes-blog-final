from django.db import models
from django.contrib.auth.models import User

def user_avatar_path(instance, filename):
    # Guarda en media/profiles/user_ID/archivo
    return f'profiles/user_{instance.user.id}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to=user_avatar_path, default='profiles/default.jpg', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    website = models.URLField(max_length=200, blank=True)
    location = models.CharField(max_length=100, blank=True)
    
    # CAMPOS QUE FALTABAN Y CAUSABAN EL ERROR:
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"