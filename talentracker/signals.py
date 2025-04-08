from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OfertaTrabajo, Usuario, Notificacion

@receiver(post_save, sender=OfertaTrabajo)
def notificar_empleados_nueva_oferta(sender, instance, created, **kwargs):
    if created:
        empleados = Usuario.objects.filter(tipo_usuario='empleado')
        for empleado in empleados:
            Notificacion.objects.create(
                usuario=empleado,
                mensaje="Tienes una nueva oferta de trabajo disponible.",
            )
