from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Crea un formulario basado en el modelo User para editar la información
class ProfileEditForm(forms.ModelForm):
    # Campos que permitiremos editar
    first_name = forms.CharField(label='Nombre', max_length=150, required=False, 
                                 widget=forms.TextInput(attrs={'class': 'form-control rounded-lg'}))
    last_name = forms.CharField(label='Apellido', max_length=150, required=False, 
                                widget=forms.TextInput(attrs={'class': 'form-control rounded-lg'}))
    email = forms.EmailField(label='Correo Electrónico', required=True, 
                             widget=forms.EmailInput(attrs={'class': 'form-control rounded-lg'}))
    
    # Nota: El campo 'username' lo excluimos aquí para evitar conflictos de validación.

    class Meta:
        model = User
        # Solo incluimos los campos que queremos que el usuario edite
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        # Validar que el nuevo email sea único (excepto si es el email actual del usuario)
        email = self.cleaned_data.get('email')
        
        # Obtenemos la instancia del usuario que estamos editando
        # self.instance es el usuario actual pasado al formulario
        user = self.instance

        if User.objects.filter(email=email).exclude(pk=user.pk).exists():
            raise ValidationError("Este correo electrónico ya está en uso por otro usuario.")
        
        return email

    def save(self, commit=True):
        # Aseguramos que el campo email no esté vacío antes de guardar
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user