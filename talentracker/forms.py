from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import FileExtensionValidator
from django.forms import inlineformset_factory
from .models import Usuario, PreguntaPerfil, OpcionPregunta, PerfilEmpresa
from .models import OfertaTrabajo, ConfiguracionNotificaciones

# --- Formulario de registro para EMPLEADOS (tu versión original sin el campo "tipo_usuario") ---
class RegistroEmpleadoForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")
    telefono = forms.CharField(max_length=15, required=False, label="Teléfono")
    fecha_nacimiento = forms.DateField(
        required=False,
        label="Fecha de nacimiento",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    curriculum = forms.FileField(
        required=False,
        widget=forms.FileInput(),
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx']),
        ]
    )

    class Meta:
        model = Usuario
        fields = [
            'username', 'email', 'password1', 'password2',
            'telefono', 'fecha_nacimiento', 'curriculum'
        ]
        labels = {
            'username': 'Nombre de usuario',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
        }

# --- Formulario para crear USUARIO EMPRESA (solo username, email, pass) ---
class RegistroEmpresaForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")

    class Meta:
        model = Usuario
        fields = [
            'username', 'email', 'password1', 'password2',
        ]
        labels = {
            'username': 'Nombre de empresa',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
        }

# --- Formulario para datos adicionales de EMPRESA ---
class PerfilEmpresaForm(forms.ModelForm):
    class Meta:
        model = PerfilEmpresa
        fields = ['nombre_empresa', 'nit', 'descripcion']
        labels = {
            'nombre_empresa': 'Nombre legal',
            'nit': 'NIT o ID fiscal',
            'descripcion': 'Descripción de la empresa',
        }

# --- Formulario para crear PREGUNTAS ---
class PreguntaPerfilForm(forms.ModelForm):
    class Meta:
        model = PreguntaPerfil
        fields = ['texto', 'obligatoria']

# --- Formset para las OPCIONES de cada pregunta ---
OpcionFormSet = inlineformset_factory(
    PreguntaPerfil,
    OpcionPregunta,
    fields=('texto',),
    extra=10,
    can_delete=False
)

class OfertaTrabajoForm(forms.ModelForm):
    HABILIDADES_CHOICES = [
        ('Python', 'Python'),
        ('SQL', 'SQL'),
        ('Comunicación', 'Comunicación'),
        ('Liderazgo', 'Liderazgo'),
        ('Ventas', 'Ventas'),
        ('Creatividad', 'Creatividad'),
    ]

    habilidades = forms.MultipleChoiceField(
        choices=HABILIDADES_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="Habilidades requeridas"
    )

    class Meta:
        model = OfertaTrabajo
        fields = [
            'titulo', 'descripcion', 'industria', 'ubicacion', 'nivel_experiencia',
            'salario_estimado', 'remoto', 'nivel_academico', 'habilidades'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded p-2'}),
            'descripcion': forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded p-2'}),
            'industria': forms.Select(attrs={'class': 'w-full border border-gray-300 rounded p-2'}),
            'ubicacion': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded p-2'}),
            'nivel_experiencia': forms.Select(attrs={'class': 'w-full border border-gray-300 rounded p-2'}),
            'salario_estimado': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded p-2', 'step': '0.01'}),
            'remoto': forms.Select(attrs={'class': 'w-full border border-gray-300 rounded p-2'}),
            'nivel_academico': forms.Select(attrs={'class': 'w-full border border-gray-300 rounded p-2'}),
        }

    def clean_habilidades(self):
        return self.cleaned_data['habilidades']  # Ya es una lista, no hay que hacer nada

 
class ConfiguracionNotificacionesForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionNotificaciones
        fields = ['recibir_notificaciones', 'notificar_por_email', 'notificar_en_plataforma']
        labels = {
            'recibir_notificaciones': 'Recibir notificaciones',
            'notificar_por_email': 'Recibir notificaciones por email',
            'notificar_en_plataforma': 'Mostrar notificaciones en la plataforma',
        }       
