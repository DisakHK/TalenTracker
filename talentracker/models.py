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
    empresa = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class Postulacion(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    oferta = models.ForeignKey(OfertaTrabajo, on_delete=models.CASCADE, related_name='postulaciones')
    fecha_postulacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} → {self.oferta.titulo}"
