from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import FileExtensionValidator
from .models import Usuario

class RegistroForm(UserCreationForm):
    # Campos adicionales para el formulario de registro
    email = forms.EmailField(required=True, label="Correo electrónico")
    telefono = forms.CharField(max_length=15, required=False, label="Teléfono")
    fecha_nacimiento = forms.DateField(
        required=False,
        label="Fecha de nacimiento",
        widget=forms.DateInput(attrs={'type': 'date'})  # Usar un input de tipo "date"
    )
    curriculum = forms.FileField( # Instancia de Parseo de Archivos
        required=False,
        widget=forms.FileInput(),
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx']),
        ] # mas opciones de cv
    )

    class Meta:
        model = Usuario
        fields = [
            'username',  # Nombre de usuario
            'email',     # Correo electrónico
            'password1', # Contraseña
            'password2', # Confirmación de contraseña
            'telefono',  # Teléfono (opcional)
            'fecha_nacimiento',  # Fecha de nacimiento (opcional)
            'curriculum',  # Archivo de currículum
        ]
        labels = {
            'username': 'Nombre de usuario',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
        }