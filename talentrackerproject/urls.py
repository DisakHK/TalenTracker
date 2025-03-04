from django.contrib import admin
from django.urls import path
from talentracker import views as talenTracker

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', talenTracker.home, name='home'),  # Ruta para la página de inicio
    path('registro/', talenTracker.registro, name='registro'),  # Ruta para el registro
]
