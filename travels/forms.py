from django import forms
from .models import TravelPost

class PostForm(forms.ModelForm):
    class Meta:
        model = TravelPost
        fields = ['title', 'subtitle', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título del viaje'}),
            'subtitle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Breve descripción'}),
            # Content usa CKEditor automáticamente si está configurado en el modelo
        }