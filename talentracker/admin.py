from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Usuario, PerfilEmpresa, OfertaTrabajo, Postulacion, PreguntaPerfil, OpcionPregunta, RespuestaPerfil, Notificacion, ConfiguracionNotificaciones, LikeOferta, VistaOferta, PreferenciaBusqueda

class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'tipo_usuario', 'is_active', 'date_joined', 'get_telefono')
    list_filter = ('tipo_usuario', 'is_active', 'date_joined', 'is_staff')
    search_fields = ('username', 'email', 'telefono')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Información personal'), {'fields': ('email', 'tipo_usuario', 'telefono', 'fecha_nacimiento', 'curriculum')}),
        (_('Permisos'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Fechas importantes'), {'fields': ('last_login', 'date_joined')}),
    )
    
    def get_telefono(self, obj):
        return obj.telefono if obj.telefono else "No especificado"
    get_telefono.short_description = 'Teléfono'
    
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if not search_term:
            return queryset, use_distinct
        
        # Permite búsqueda por tipo de usuario si se escribe 'candidato' o 'empleador'
        if search_term.lower() in ['candidato', 'empleado']:
            queryset |= self.model.objects.filter(tipo_usuario='empleado')
        elif search_term.lower() in ['empleador', 'empresa']:
            queryset |= self.model.objects.filter(tipo_usuario='empresa')
            
        return queryset, use_distinct

class PerfilEmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre_empresa', 'nit', 'get_usuario_email')
    search_fields = ('nombre_empresa', 'nit', 'usuario__email')
    
    def get_usuario_email(self, obj):
        return obj.usuario.email
    get_usuario_email.short_description = 'Email'

class OfertaTrabajoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'get_empresa', 'industria', 'ubicacion', 'nivel_experiencia', 'fecha_creacion')
    list_filter = ('industria', 'nivel_experiencia', 'remoto', 'nivel_academico', 'fecha_creacion')
    search_fields = ('titulo', 'descripcion', 'empresa__username')
    date_hierarchy = 'fecha_creacion'
    
    def get_empresa(self, obj):
        return obj.empresa.username
    get_empresa.short_description = 'Empresa'

class PostulacionAdmin(admin.ModelAdmin):
    list_display = ('get_usuario', 'get_oferta', 'fecha_postulacion')
    list_filter = ('fecha_postulacion',)
    
    def get_usuario(self, obj):
        return obj.usuario.username
    get_usuario.short_description = 'Usuario'
    
    def get_oferta(self, obj):
        return obj.oferta.titulo
    get_oferta.short_description = 'Oferta'

class PreguntaPerfilAdmin(admin.ModelAdmin):
    list_display = ('texto', 'obligatoria')

class OpcionPreguntaAdmin(admin.ModelAdmin):
    list_display = ('texto', 'get_pregunta')
    
    def get_pregunta(self, obj):
        return obj.pregunta.texto
    get_pregunta.short_description = 'Pregunta'

class RespuestaPerfilAdmin(admin.ModelAdmin):
    list_display = ('get_usuario', 'get_pregunta', 'get_opcion')
    
    def get_usuario(self, obj):
        return obj.usuario.username
    get_usuario.short_description = 'Usuario'
    
    def get_pregunta(self, obj):
        return obj.pregunta.texto
    get_pregunta.short_description = 'Pregunta'
    
    def get_opcion(self, obj):
        return obj.opcion.texto if obj.opcion else "Sin respuesta"
    get_opcion.short_description = 'Respuesta'

class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('get_usuario', 'tipo', 'leida', 'fecha_creacion')
    list_filter = ('tipo', 'leida', 'fecha_creacion')
    
    def get_usuario(self, obj):
        return obj.usuario.username
    get_usuario.short_description = 'Usuario'

# Registrar modelos en el admin
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(PerfilEmpresa, PerfilEmpresaAdmin)
admin.site.register(OfertaTrabajo, OfertaTrabajoAdmin)
admin.site.register(Postulacion, PostulacionAdmin)
admin.site.register(PreguntaPerfil, PreguntaPerfilAdmin)
admin.site.register(OpcionPregunta, OpcionPreguntaAdmin)
admin.site.register(RespuestaPerfil, RespuestaPerfilAdmin)
admin.site.register(Notificacion, NotificacionAdmin)
admin.site.register(ConfiguracionNotificaciones)
admin.site.register(LikeOferta)
admin.site.register(VistaOferta)
admin.site.register(PreferenciaBusqueda)
