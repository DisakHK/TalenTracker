from django.contrib import admin
from django.urls import path
from talentracker import views as talenTracker

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', talenTracker.home, name='home'),  # Ruta para la página de inicio
    path('registro/', talenTracker.registro, name='registro'),  # Ruta para el registro
    path('iniciar-sesion/', talenTracker.iniciar_sesion, name='iniciar_sesion'),    # Ruta para iniciar sesión
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)