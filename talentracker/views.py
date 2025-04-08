from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Usuario, OfertaTrabajo, Postulacion
from django.contrib import messages

from .forms import (
    RegistroEmpleadoForm, RegistroEmpresaForm,
    PerfilEmpresaForm, PreguntaPerfilForm, OpcionFormSet,
    OfertaTrabajoForm
)
from .models import (
    Usuario, PreguntaPerfil, RespuestaPerfil, OpcionPregunta,
    OfertaTrabajo, Postulacion,
    ConfiguracionNotificaciones, Notificacion
)
from .forms import ConfiguracionNotificacionesForm

# Home
def home(request):
    return render(request, 'home.html')

# Elección de tipo de usuario
def elegir_tipo_usuario(request):
    return render(request, 'elegir_tipo.html')

@login_required
def dashboard(request):
    if request.user.tipo_usuario == 'empresa':
        return redirect('dashboard_empresa')

    ofertas = OfertaTrabajo.objects.all().order_by('-fecha_creacion')
    postuladas = Postulacion.objects.filter(usuario=request.user).values_list('oferta_id', flat=True)
    
    # Aquí agregamos las notificaciones del usuario
    notificaciones = Notificacion.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    leida = notificaciones.filter(leida=False).count()
 
    return render(request, 'dashboard_empleado.html', {
        'ofertas': ofertas,
        'postuladas': postuladas,
        'notificaciones': notificaciones,
        'leida': leida
    })
    
# Dashboard empresa
@login_required
def dashboard_empresa(request):
    if request.user.tipo_usuario != 'empresa':
        return redirect('dashboard')

    ofertas = OfertaTrabajo.objects.filter(empresa=request.user).prefetch_related('postulaciones__usuario')
    return render(request, 'dashboard_empresa.html', {'ofertas': ofertas})

@login_required
def crear_oferta(request):
    if request.user.tipo_usuario != 'empresa':
        return redirect('dashboard')

    if request.method == 'POST':
        form = OfertaTrabajoForm(request.POST)
        if form.is_valid():
            oferta = form.save(commit=False)
            oferta.empresa = request.user
            oferta.save()
            
            # El signal se encargará de las notificaciones
            messages.success(request, 'Oferta creada exitosamente. Los empleados serán notificados.')
            return redirect('dashboard_empresa')
    else:
        form = OfertaTrabajoForm()
    
    return render(request, 'crear_oferta.html', {'form': form})
       
@login_required
def eliminar_oferta(request, oferta_id):
    oferta = get_object_or_404(OfertaTrabajo, id=oferta_id)
    oferta.delete()
    return redirect('dashboard_empresa')
    
# Postularse a una oferta
@login_required
def postular(request, oferta_id):
    if request.user.tipo_usuario != 'empleado':
        return redirect('dashboard')

    oferta = get_object_or_404(OfertaTrabajo, id=oferta_id)
    Postulacion.objects.get_or_create(usuario=request.user, oferta=oferta)
    
     # Borrar notificaciones del usuario
    Notificacion.objects.filter(usuario=request.user).delete()
    
    return redirect('dashboard')



# Registro empleado
def registro_empleado(request):
    if request.method == 'POST':
        form = RegistroEmpleadoForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.tipo_usuario = 'empleado'
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistroEmpleadoForm()
    return render(request, 'registro_empleado.html', {'form': form})

# Registro empresa + perfil
def registro_empresa(request):
    if request.method == 'POST':
        user_form = RegistroEmpresaForm(request.POST)
        perfil_form = PerfilEmpresaForm(request.POST)
        if user_form.is_valid() and perfil_form.is_valid():
            user = user_form.save(commit=False)
            user.tipo_usuario = 'empresa'
            user.save()

            perfil = perfil_form.save(commit=False)
            perfil.usuario = user
            perfil.save()

            login(request, user)
            return redirect('dashboard_empresa')
    else:
        user_form = RegistroEmpresaForm()
        perfil_form = PerfilEmpresaForm()
    return render(request, 'registro_empresa.html', {
        'user_form': user_form,
        'perfil_form': perfil_form
    })

# Iniciar sesión
def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        return render(request, 'talentracker/iniciar_sesion.html', {'error': 'Usuario o contraseña incorrectos'})
    return render(request, 'iniciar_sesion.html')

# Cerrar sesión
def cerrar_sesion(request):
    logout(request)
    return redirect('home')

# Página admin para preguntas
@user_passes_test(lambda u: u.is_superuser)
def admin_preguntas(request):
    if request.method == 'POST':
        form = PreguntaPerfilForm(request.POST)
        if form.is_valid():
            pregunta = form.save(commit=False)
            formset = OpcionFormSet(request.POST, instance=pregunta)
            if formset.is_valid():
                pregunta.save()
                formset.save()
                return redirect('admin_preguntas')
    else:
        form = PreguntaPerfilForm()
        formset = OpcionFormSet()

    preguntas = PreguntaPerfil.objects.prefetch_related('opciones')
    return render(request, 'admin_preguntas.html', {
        'form': form,
        'formset': formset,
        'preguntas': preguntas
    })

# Eliminar pregunta
@user_passes_test(lambda u: u.is_superuser)
def eliminar_pregunta(request, pregunta_id):
    try:
        pregunta = PreguntaPerfil.objects.get(id=pregunta_id)
        pregunta.delete()
    except PreguntaPerfil.DoesNotExist:
        pass
    return redirect('admin_preguntas')

# Guardar respuestas de perfil
@login_required
def guardar_respuestas(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('pregunta_') and value:
                pregunta_id = int(key.split('_')[1])
                try:
                    opcion_id = int(value)
                    RespuestaPerfil.objects.update_or_create(
                        usuario=request.user,
                        pregunta_id=pregunta_id,
                        defaults={'opcion_id': opcion_id}
                    )
                except (ValueError, OpcionPregunta.DoesNotExist):
                    continue
        return redirect('home')
    return redirect('home')

# Vista extra para empresa si no querés usar dashboard_empresa directamente
@login_required
def ver_ofertas_empresa(request):
    return dashboard_empresa(request)  # se puede eliminar si no se usa por separado

# Configuración de notificaciones
@login_required
def configurar_notificaciones(request):
    try:
        config = ConfiguracionNotificaciones.objects.get(usuario=request.user)
    except ConfiguracionNotificaciones.DoesNotExist:
        config = ConfiguracionNotificaciones.objects.create(usuario=request.user)

    if request.method == 'POST':
        form = ConfiguracionNotificacionesForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ConfiguracionNotificacionesForm(instance=config)

    return render(request, 'configurar_notificaciones.html', {'form': form})

# Ver notificaciones
@login_required
def ver_notificaciones(request):
    notificaciones = Notificacion.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'notificaciones.html', {'notificaciones': notificaciones})

@login_required
def marcar_leida(request, notificacion_id):
    notificacion = get_object_or_404(Notificacion, id=notificacion_id, usuario=request.user)
    notificacion.leida = True
    notificacion.save()
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

def obtener_preferencias_usuario(usuario):
    respuestas = RespuestaPerfil.objects.filter(usuario=usuario).select_related('pregunta', 'opcion')
    preferencias = {r.pregunta.texto: r.opcion.texto for r in respuestas}
    return preferencias