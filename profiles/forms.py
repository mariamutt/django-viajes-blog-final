from django import forms
from .models import Profile
from django.contrib.auth.models import User

# Formulario para actualizar el modelo Profile
class ProfileUpdateForm(forms.ModelForm):
    # Se incluye el campo de avatar que es un ImageField
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'location', 'birth_date']
        
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Cuéntanos sobre tus aventuras...'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad, País...'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

# Opcional: Si quieres permitir cambiar nombre, apellido y email del modelo User
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }