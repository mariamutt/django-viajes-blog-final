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
    
    # Rutas para la app de Cuentas (registro, perfil)
    path('accounts/', include('accounts.urls', namespace='accounts')), 
    
    # Rutas para la app de Posts de Viaje (CRUD)
    path('travels/', include('travels.urls', namespace='travels')),
    
    # Rutas para la app profiles
    path('profiles/', include('profiles.urls', namespace='profiles')),
    
    # Rutas para la app de Mensajería (inbox)
    path('inbox/', include('inbox.urls')), 
    
    # Ruta de inicio y about
    path('', views.home, name='home'),
    path('about/', views.about, name='about'), 
]

# Configuración para servir archivos multimedia (imágenes) en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)