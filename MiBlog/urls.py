from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views # Importar las vistas del proyecto principal

urlpatterns = [
    # Rutas de administración
    path('admin/', admin.site.urls),
    
    # Rutas de autenticación de Django (login, logout, password reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Rutas para la app de Cuentas (registro y perfil)
    path('accounts/', include('accounts.urls')), 
    
    # Rutas para la app de Posts de Viaje (CRUD)
    path('posts/', include('travels.urls')),
    
    # Rutas para la app de Mensajería (inbox)
    path('inbox/', include('inbox.urls')), # <--- AÑADIDO: Conecta la app inbox
    
    # Ruta de inicio y about
    path('', views.home, name='home'),
    path('about/', views.about, name='about'), # Asegúrate de que esta URL exista
]

# Configuración para servir archivos multimedia (imágenes) en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)