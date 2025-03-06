from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

# Registra el modelo Usuario en el panel de administración
admin.site.register(Usuario, UserAdmin)

# Register your models here.
