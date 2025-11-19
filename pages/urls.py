from django.urls import path
from .views import HomePageView, AboutPageView

app_name = 'pages'

urlpatterns = [
    # Ruta para la página 'Acerca de' (Ej: /about/)
    path('about/', AboutPageView.as_view(), name='about'),
    
    # Esta es la ruta principal (Ej: /)
    path('', HomePageView.as_view(), name='home'),
]