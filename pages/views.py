from django.views.generic import TemplateView

class HomePageView(TemplateView):
    """Muestra la página de inicio."""
    template_name = "home.html" 

class AboutPageView(TemplateView):
    """Muestra la página 'Acerca de'."""
    template_name = "about.html"