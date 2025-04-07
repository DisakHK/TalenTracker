from django.contrib import admin
from .models import PreguntaPerfil, RespuestaPerfil, Usuario

# Este sí usa UserAdmin porque extiende de AbstractUser
from django.contrib.auth.admin import UserAdmin
admin.site.register(Usuario, UserAdmin)

# Estos dos usan el admin normal
admin.site.register(PreguntaPerfil)
admin.site.register(RespuestaPerfil)