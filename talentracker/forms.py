from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import FileExtensionValidator
from django.forms import inlineformset_factory
from .models import Usuario, PreguntaPerfil, OpcionPregunta, PerfilEmpresa, OfertaTrabajo, ConfiguracionNotificaciones, PreferenciaBusqueda

# --- Formulario de registro para EMPLEADOS (tu versión original sin el campo "tipo_usuario") ---
class RegistroEmpleadoForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="Nombre")
    last_name = forms.CharField(max_length=30, required=True, label="Apellido")
    email = forms.EmailField(required=True, label="Correo electrónico")
    telefono = forms.CharField(max_length=15, required=False, label="Teléfono")
    fecha_nacimiento = forms.DateField(
        required=False,
        label="Fecha de nacimiento",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    genero = forms.ChoiceField(
        choices=[('', 'Seleccionar'), ('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')],
        required=False,
        label="Género"
    )
    biografia = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}), 
        required=False, 
        label="Biografía/Resumen profesional",
        help_text="Escribe un breve resumen sobre ti, tus habilidades y experiencia profesional."
    )
    curriculum = forms.FileField(
        required=False,
        widget=forms.FileInput(),
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx']),
        ],
        label="Curriculum (PDF, DOC, DOCX)"
    )

    class Meta:
        model = Usuario
        fields = [
            'first_name', 'last_name', 'username', 'email', 'password1', 'password2',
            'telefono', 'fecha_nacimiento', 'genero', 'biografia', 'curriculum'
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
    # Habilidades blandas (siempre presentes)
    HABILIDADES_BLANDAS = [
        ('Comunicación', 'Comunicación'),
        ('Liderazgo', 'Liderazgo'),
        ('Trabajo en equipo', 'Trabajo en equipo'),
        ('Resolución de problemas', 'Resolución de problemas'),
        ('Creatividad', 'Creatividad'),
        ('Adaptabilidad', 'Adaptabilidad'),
        ('Gestión del tiempo', 'Gestión del tiempo'),
    ]
    
    # Habilidades por industria
    HABILIDADES_POR_INDUSTRIA = {
        'tecnologia': [
            ('Python', 'Python'),
            ('Java', 'Java'),
            ('JavaScript', 'JavaScript'),
            ('SQL', 'SQL'),
            ('DevOps', 'DevOps'),
            ('React', 'React'),
            ('Node.js', 'Node.js'),
            ('AWS', 'AWS'),
        ],
        'salud': [
            ('Primeros auxilios', 'Primeros auxilios'),
            ('Conocimientos médicos', 'Conocimientos médicos'),
            ('Atención al paciente', 'Atención al paciente'),
            ('Gestión sanitaria', 'Gestión sanitaria'),
        ],
        'finanzas': [
            ('Excel', 'Excel'),
            ('Contabilidad', 'Contabilidad'),
            ('Análisis financiero', 'Análisis financiero'),
            ('SAP', 'SAP'),
            ('Gestión de riesgos', 'Gestión de riesgos'),
        ],
        'educacion': [
            ('Pedagogía', 'Pedagogía'),
            ('Diseño curricular', 'Diseño curricular'),
            ('Gestión del aula', 'Gestión del aula'),
            ('E-learning', 'E-learning'),
        ],
        'servicios': [
            ('Atención al cliente', 'Atención al cliente'),
            ('Ventas', 'Ventas'),
            ('Marketing', 'Marketing'),
            ('Gestión de reclamaciones', 'Gestión de reclamaciones'),
        ],
        'otros': [
            ('Gestión de proyectos', 'Gestión de proyectos'),
            ('Ventas', 'Ventas'),
            ('Marketing', 'Marketing'),
        ],
    }
    
    # Campo para habilidades personalizadas
    habilidades_personalizadas = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Ej: Excel, Photoshop (separadas por comas)'}),
        label="Otras habilidades (separadas por comas)"
    )

    class Meta:
        model = OfertaTrabajo
        fields = [
            'titulo', 'descripcion', 'industria', 'ubicacion', 'nivel_experiencia',
            'salario_estimado', 'remoto', 'nivel_academico', 'habilidades', 'habilidades_personalizadas'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded p-2'}),
            'descripcion': forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded p-2'}),
            'industria': forms.Select(attrs={'class': 'w-full border border-gray-300 rounded p-2', 'id': 'id_industria'}),
            'ubicacion': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded p-2'}),
            'nivel_experiencia': forms.Select(attrs={'class': 'w-full border border-gray-300 rounded p-2'}),
            'salario_estimado': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded p-2', 'step': '0.01'}),
            'remoto': forms.Select(attrs={'class': 'w-full border border-gray-300 rounded p-2'}),
            'nivel_academico': forms.Select(attrs={'class': 'w-full border border-gray-300 rounded p-2'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Crear lista de todas las habilidades conocidas
        todas_las_habilidades = list(self.HABILIDADES_BLANDAS)
        for industria_habilidades in self.HABILIDADES_POR_INDUSTRIA.values():
            todas_las_habilidades.extend(industria_habilidades)
        
        # Establecer todas las habilidades como opciones válidas
        self.fields['habilidades'] = forms.MultipleChoiceField(
            choices=todas_las_habilidades,
            widget=forms.CheckboxSelectMultiple,
            label="Habilidades requeridas",
            required=False
        )
        
        # Si es una edición y hay datos iniciales
        if 'instance' in kwargs and kwargs['instance']:
            instance = kwargs['instance']
            # Establecer habilidades iniciales si existen
            if hasattr(instance, 'habilidades') and instance.habilidades:
                # Filtrar habilidades personalizadas
                habilidades_conocidas = []
                habilidades_personalizadas = []
                
                # Crear lista de todas las habilidades conocidas como valores
                todas_habilidades_conocidas = [h[0] for h in todas_las_habilidades]
                
                # Separar habilidades conocidas de personalizadas
                for hab in instance.habilidades:
                    if hab in todas_habilidades_conocidas:
                        habilidades_conocidas.append(hab)
                    else:
                        habilidades_personalizadas.append(hab)
                
                # Establecer valores iniciales
                self.initial['habilidades'] = habilidades_conocidas
                self.initial['habilidades_personalizadas'] = ', '.join(habilidades_personalizadas)

    def clean(self):
        cleaned_data = super().clean()
        
        # Obtener habilidades seleccionadas
        habilidades = cleaned_data.get('habilidades', [])
        
        # Obtener y procesar habilidades personalizadas
        habilidades_personalizadas = cleaned_data.get('habilidades_personalizadas', '')
        if habilidades_personalizadas:
            # Convertir a lista y limpiar espacios en blanco
            habs_personalizadas_lista = [h.strip() for h in habilidades_personalizadas.split(',') if h.strip()]
            # Combinar con las habilidades seleccionadas
            habilidades = list(habilidades) + habs_personalizadas_lista
        
        # Guardar las habilidades combinadas en cleaned_data
        cleaned_data['habilidades'] = habilidades
        
        return cleaned_data

class ConfiguracionNotificacionesForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionNotificaciones
        fields = ['recibir_notificaciones', 'notificar_por_email', 'notificar_en_plataforma']
        labels = {
            'recibir_notificaciones': 'Recibir notificaciones',
            'notificar_por_email': 'Recibir notificaciones por email',
            'notificar_en_plataforma': 'Mostrar notificaciones en la plataforma',
        }       

class PreferenciaBusquedaForm(forms.ModelForm):
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
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select'})
    )
    
    predeterminado = forms.BooleanField(
        required=False,
        label="Usar como filtro predeterminado",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = PreferenciaBusqueda
        fields = [
            'nombre', 'nivel_experiencia', 'industria', 'ubicacion',
            'remoto', 'nivel_academico', 'habilidades', 'predeterminado'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'nivel_experiencia': forms.Select(attrs={'class': 'form-select'}),
            'industria': forms.Select(attrs={'class': 'form-select'}),
            'remoto': forms.Select(attrs={'class': 'form-select'}),
            'nivel_academico': forms.Select(attrs={'class': 'form-select'}),
        }
        
    def clean_habilidades(self):
        return list(self.cleaned_data['habilidades'])       

# --- Formulario para editar perfil de EMPLEADO ---
class EditarPerfilEmpleadoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Correo electrónico")
    telefono = forms.CharField(max_length=15, required=False, label="Teléfono")
    fecha_nacimiento = forms.DateField(
        required=False,
        label="Fecha de nacimiento",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    genero = forms.ChoiceField(
        choices=[('', 'Seleccionar'), ('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')],
        required=False,
        label="Género"
    )
    curriculum = forms.FileField(
        required=False,
        widget=forms.FileInput(),
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx']),
        ],
        label="Curriculum (PDF, DOC, DOCX)"
    )
    first_name = forms.CharField(max_length=30, required=False, label="Nombre")
    last_name = forms.CharField(max_length=30, required=False, label="Apellido")
    biografia = forms.CharField(widget=forms.Textarea, required=False, label="Biografía/Resumen profesional")

    class Meta:
        model = Usuario
        fields = [
            'first_name', 'last_name', 'email', 'telefono', 
            'fecha_nacimiento', 'genero', 'biografia', 'curriculum'
        ]
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
        }
