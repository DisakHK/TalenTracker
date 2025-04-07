from django.contrib import admin
from django.urls import path
from talentracker import views as talenTracker
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', talenTracker.home, name='home'),

    # Autenticación
    path('iniciar-sesion/', talenTracker.iniciar_sesion, name='iniciar_sesion'),
    path('cerrar-sesion/', talenTracker.cerrar_sesion, name='cerrar_sesion'),

    # Registro por tipo de usuario
    path('elige-tipo/', talenTracker.elegir_tipo_usuario, name='elegir_tipo_usuario'),
    path('registro/empleado/', talenTracker.registro_empleado, name='registro_empleado'),
    path('registro/empresa/', talenTracker.registro_empresa, name='registro_empresa'),

    # Dashboards
    path('dashboard/', talenTracker.dashboard, name='dashboard'),
    path('empresa/dashboard/', talenTracker.dashboard_empresa, name='dashboard_empresa'),

    # Ofertas de trabajo
    path('empresa/crear-oferta/', talenTracker.crear_oferta, name='crear_oferta'),
    path('postular/<int:oferta_id>/', talenTracker.postular, name='postular'),

    # Preguntas de perfil (admin)
    path('guardar-respuestas/', talenTracker.guardar_respuestas, name='guardar_respuestas'),
    path('admin-preguntas/', talenTracker.admin_preguntas, name='admin_preguntas'),
    path('eliminar-pregunta/<int:pregunta_id>/', talenTracker.eliminar_pregunta, name='eliminar_pregunta'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)