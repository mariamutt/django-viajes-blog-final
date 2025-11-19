from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home, about # Asegúrate de crear estas vistas simples

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('about/', about, name='about'),
    
    # Rutas de las Apps
    path('accounts/', include('accounts.urls')), # Auth
    path('profiles/', include('profiles.urls')), # Perfiles
    path('pages/', include('travels.urls')),     # Blog (según consigna: pages/)
    path('inbox/', include('inbox.urls')),       # Mensajería
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)