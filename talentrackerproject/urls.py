from django.contrib import admin
from django.urls import path
from talentracker import views as talenTracker
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', talenTracker.home, name='home'),

    # Autenticación
    path('iniciar_sesion/', talenTracker.iniciar_sesion, name='iniciar_sesion'),
    path('cerrar_sesion/', talenTracker.cerrar_sesion, name='cerrar_sesion'),

    # Registro por tipo de usuario
    path('elige-tipo/', talenTracker.elegir_tipo_usuario, name='elegir_tipo_usuario'),
    path('registro/empleado/', talenTracker.registro_empleado, name='registro_empleado'),
    path('registro/empresa/', talenTracker.registro_empresa, name='registro_empresa'),

    # Dashboards
    path('dashboard/', talenTracker.dashboard, name='dashboard'),
    path('empresa/dashboard/', talenTracker.dashboard_empresa, name='dashboard_empresa'),
    path('ofertas/', talenTracker.dashboard, name='ofertas'),

    # Ofertas de trabajo
    path('empresa/crear-oferta/', talenTracker.crear_oferta, name='crear_oferta'),
    path('empresa/editar-oferta/<int:oferta_id>/', talenTracker.editar_oferta, name='editar_oferta'),
    path('postular/<int:oferta_id>/', talenTracker.postular, name='postular'),
    path('oferta/<int:oferta_id>/eliminar/',talenTracker.eliminar_oferta, name='eliminar_oferta'),
    path('oferta/<int:oferta_id>/', talenTracker.ver_detalle_oferta, name='ver_detalle_oferta'),
   
    # Preguntas de perfil (admin)
    path('guardar-respuestas/', talenTracker.guardar_respuestas, name='guardar_respuestas'),
    path('admin-preguntas/', talenTracker.admin_preguntas, name='admin_preguntas'),
    path('eliminar-pregunta/<int:pregunta_id>/', talenTracker.eliminar_pregunta, name='eliminar_pregunta'),
    
    # Notificaciones
    path('configurar-notificaciones/', talenTracker.configurar_notificaciones, name='configurar_notificaciones'),
    path('notificaciones/', talenTracker.ver_notificaciones, name='ver_notificaciones'),
    path('notificaciones/marcar-leida/<int:notificacion_id>/', talenTracker.marcar_leida, name='marcar_leida'),

    # Favoritos / Likes
    path('toggle-like/<int:oferta_id>/', talenTracker.toggle_like, name='toggle_like'),
    path('favoritos/', talenTracker.favoritos, name='favoritos'),

    # Empresa
    path('mis-ofertas/', talenTracker.ver_ofertas_empresa, name='ver_ofertas_empresa'),
    
    # Preferencias de búsqueda
    path('preferencias-busqueda/', talenTracker.preferencias_busqueda, name='preferencias_busqueda'),
    path('preferencias-busqueda/editar/<int:preferencia_id>/', talenTracker.editar_preferencia, name='editar_preferencia'),
    path('preferencias-busqueda/eliminar/<int:preferencia_id>/', talenTracker.eliminar_preferencia, name='eliminar_preferencia'),
    path('preferencias-busqueda/aplicar/<int:preferencia_id>/', talenTracker.aplicar_preferencia, name='aplicar_preferencia'),
    
    # Reportes
    path('reportes/', talenTracker.generar_reporte, name='generar_reporte'),
    path('reportes/descargar-pdf/', talenTracker.descargar_reporte_pdf, name='descargar_reporte_pdf'),
    
    # Perfiles
    path('perfil/editar/', talenTracker.editar_perfil_empleado, name='editar_perfil_empleado'),
    path('perfil/profesional/editar/', talenTracker.editar_perfil_profesional, name='editar_perfil_profesional'),
    path('perfil/', talenTracker.ver_perfil_empleado, name='ver_perfil_empleado'),
    path('empresa/oferta/<int:oferta_id>/postulante/<int:usuario_id>/', talenTracker.ver_detalle_postulante, name='ver_detalle_postulante'),

    # URLs para tracking y recomendaciones
    path('iniciar-vista/<int:oferta_id>/', talenTracker.iniciar_vista_oferta, name='iniciar_vista_oferta'),
    path('finalizar-vista/<int:vista_id>/', talenTracker.finalizar_vista_oferta, name='finalizar_vista_oferta'),
    path('recomendaciones/', talenTracker.recomendaciones, name='recomendaciones'),
]

# Configuración para servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 