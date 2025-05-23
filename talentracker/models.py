from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# Create your models here.
class Usuario(AbstractUser):
    TIPO_USUARIO_CHOICES = [
        ('empleado', 'Empleado'),
        ('empresa', 'Empresa'),
    ]
    tipo_usuario = models.CharField(max_length=10, choices=TIPO_USUARIO_CHOICES, default='empleado')
    
    telefono = models.CharField(max_length=15, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    curriculum = models.FileField(upload_to='curriculos/', null=True, blank=True)
    genero = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], blank=True, null=True)
    biografia = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username

class PerfilEmpresa(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nombre_empresa = models.CharField(max_length=100)
    nit = models.CharField(max_length=20)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre_empresa

class PreguntaPerfil(models.Model):
    texto = models.CharField(max_length=255)
    obligatoria = models.BooleanField(default=False)

    def __str__(self):
        return self.texto

class OpcionPregunta(models.Model):
    pregunta = models.ForeignKey(PreguntaPerfil, related_name='opciones', on_delete=models.CASCADE)
    texto = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.pregunta.texto} → {self.texto}"

class RespuestaPerfil(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(PreguntaPerfil, on_delete=models.CASCADE)
    opcion = models.ForeignKey(OpcionPregunta, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.pregunta.texto} - {self.opcion.texto if self.opcion else 'Sin respuesta'}"

class OfertaTrabajo(models.Model):
    INDUSTRIAS = [
        ('tecnologia', 'Tecnología'),
        ('salud', 'Salud'),
        ('finanzas', 'Finanzas'),
        ('educacion', 'Educación'),
        ('servicios', 'Servicios'),
        ('otros', 'Otros'),
    ]

    EXPERIENCIA = [
        ('junior', 'Junior'),
        ('intermedio', 'Intermedio'),
        ('senior', 'Senior'),
    ]

    empresa = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    industria = models.CharField(max_length=50, choices=INDUSTRIAS, default='otros')
    ubicacion = models.CharField(max_length=100, default='No especificada')
    nivel_experiencia = models.CharField(max_length=20, choices=EXPERIENCIA, default='junior')
    salario_estimado = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    remoto = models.CharField(max_length=20, choices=[('presencial', 'Presencial'), ('remoto', 'Remoto'), ('hibrido', 'Híbrido')], default='presencial')
    nivel_academico = models.CharField(max_length=20, choices=[
        ('ninguno', 'Ninguno'),
        ('secundaria', 'Secundaria'),
        ('tecnico', 'Técnico'),
        ('universitario', 'Universitario'),
        ('posgrado', 'Posgrado')
    ], default='ninguno')
    habilidades = models.JSONField(default=list)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class Postulacion(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    oferta = models.ForeignKey(OfertaTrabajo, on_delete=models.CASCADE, related_name='postulaciones')
    fecha_postulacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} → {self.oferta.titulo}"
    
# En models.py, agregar al final:

class ConfiguracionNotificaciones(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='config_notificaciones')
    recibir_notificaciones = models.BooleanField(default=True)
    notificar_por_email = models.BooleanField(default=True)
    notificar_en_plataforma = models.BooleanField(default=True)

    def __str__(self):
        return f"Configuración de {self.usuario.username}"

# configurar el envío de notificaciones 
class Notificacion(models.Model):
    TIPO_CHOICES = [
        ('vacante', 'Nueva vacante coincidente'),
        ('postulacion', 'Actualización de postulación'),
    ]
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='notificaciones')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    mensaje = models.TextField()
    oferta = models.ForeignKey(OfertaTrabajo, on_delete=models.CASCADE, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.get_tipo_display()}"

# Add this as a separate model class (not nested)
class LikeOferta(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    oferta = models.ForeignKey(OfertaTrabajo, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'oferta')  # Evita duplicados
        verbose_name = 'Like a oferta'
        verbose_name_plural = 'Likes a ofertas'

    def __str__(self):
        return f"{self.usuario.username} like a {self.oferta.titulo}"

# Modelo para trackear las vistas de ofertas y tiempo de interacción
class VistaOferta(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    oferta = models.ForeignKey(OfertaTrabajo, on_delete=models.CASCADE)
    timestamp_inicio = models.DateTimeField(auto_now_add=True)
    duracion_segundos = models.IntegerField(default=0)  # Duración en segundos que el usuario vio la oferta
    interaccion_completa = models.BooleanField(default=False)  # Si el usuario terminó de ver la oferta
    
    class Meta:
        verbose_name = 'Vista de oferta'
        verbose_name_plural = 'Vistas de ofertas'
        
    def __str__(self):
        return f"{self.usuario.username} vio {self.oferta.titulo} por {self.duracion_segundos}s"

class PreferenciaBusqueda(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='preferencias_busqueda')
    nombre = models.CharField(max_length=100)
    nivel_experiencia = models.CharField(max_length=20, choices=OfertaTrabajo.EXPERIENCIA, blank=True, null=True)
    industria = models.CharField(max_length=50, choices=OfertaTrabajo.INDUSTRIAS, blank=True, null=True)
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    remoto = models.CharField(max_length=20, choices=[('presencial', 'Presencial'), ('remoto', 'Remoto'), ('hibrido', 'Híbrido')], blank=True, null=True)
    nivel_academico = models.CharField(max_length=20, choices=[
        ('ninguno', 'Ninguno'),
        ('secundaria', 'Secundaria'),
        ('tecnico', 'Técnico'),
        ('universitario', 'Universitario'),
        ('posgrado', 'Posgrado')
    ], blank=True, null=True)
    habilidades = models.JSONField(default=list, blank=True)
    predeterminado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Preferencia de búsqueda'
        verbose_name_plural = 'Preferencias de búsqueda'
        
    def __str__(self):
        return f"{self.nombre} - {self.usuario.username}"
        
    def save(self, *args, **kwargs):
        # Si se marca como predeterminado, desmarcar otros predeterminados del usuario
        if self.predeterminado:
            PreferenciaBusqueda.objects.filter(
                usuario=self.usuario, 
                predeterminado=True
            ).exclude(pk=self.pk).update(predeterminado=False)
        super().save(*args, **kwargs)

class PerfilProfesional(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    habilidades = models.JSONField(default=list)
    nivel_experiencia = models.CharField(max_length=20, choices=[
        ('junior', 'Junior'),
        ('intermedio', 'Intermedio'),
        ('senior', 'Senior')
    ], default='junior')
    ubicacion = models.CharField(max_length=100, default='No especificada')
    preferencia_modalidad = models.CharField(max_length=20, choices=[
        ('presencial', 'Presencial'),
        ('remoto', 'Remoto'),
        ('mixto', 'Mixto')
    ], default='presencial')
    nivel_academico = models.CharField(max_length=20, choices=[
        ('ninguno', 'Ninguno'),
        ('secundaria', 'Secundaria'),
        ('tecnico', 'Técnico'),
        ('universitario', 'Universitario'),
        ('posgrado', 'Posgrado')
    ], default='ninguno')
    
    def __str__(self):
        return f"Perfil de {self.usuario.username}"