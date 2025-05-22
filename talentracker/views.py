from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import (
    Usuario, PreguntaPerfil, RespuestaPerfil, OpcionPregunta,
    OfertaTrabajo, Postulacion, ConfiguracionNotificaciones, Notificacion,
    LikeOferta, PerfilEmpresa, PreferenciaBusqueda, VistaOferta
)
from .forms import (
    RegistroEmpleadoForm, RegistroEmpresaForm, PerfilEmpresaForm,
    PreguntaPerfilForm, OpcionFormSet, OfertaTrabajoForm,
    ConfiguracionNotificacionesForm, PreferenciaBusquedaForm, EditarPerfilEmpleadoForm
)
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.paginator import Paginator
from django.template.loader import get_template
from django.utils import timezone
from datetime import datetime, timedelta
from xhtml2pdf import pisa
from io import BytesIO
import json
from django.db.models import Count, Q, F, Sum, Avg, ExpressionWrapper, FloatField
from django.db.models.functions import TruncDay, TruncMonth
from django.db.utils import IntegrityError
import random

# Home
def home(request):
    return render(request, 'home.html')

# Elección de tipo de usuario
def elegir_tipo_usuario(request):
    return render(request, 'elegir_tipo.html')

@login_required
def dashboard(request):
    if request.user.tipo_usuario == 'empresa':
        return redirect('dashboard_empresa')  # Evita mostrar dashboard de empleados a empresas

    ofertas = OfertaTrabajo.objects.all().order_by('-fecha_creacion')

    # Filtros
    industria = request.GET.get('industria')
    ubicacion = request.GET.get('ubicacion')
    experiencia = request.GET.get('nivel_experiencia')
    remoto = request.GET.get('remoto')
    nivel_academico = request.GET.get('nivel_academico')

    if industria:
        ofertas = ofertas.filter(industria=industria)
    if ubicacion:
        ofertas = ofertas.filter(ubicacion__icontains=ubicacion)
    if experiencia:
        ofertas = ofertas.filter(nivel_experiencia=experiencia)
    if remoto:
        ofertas = ofertas.filter(remoto=remoto)
    if nivel_academico:
        ofertas = ofertas.filter(nivel_academico=nivel_academico)

    postuladas = Postulacion.objects.filter(usuario=request.user).values_list('oferta_id', flat=True)
    likes = LikeOferta.objects.filter(usuario=request.user).values_list('oferta_id', flat=True)
    notificaciones = Notificacion.objects.filter(usuario=request.user)

    context = {
        'ofertas': ofertas,
        'industria': industria,
        'ubicacion': ubicacion,
        'nivel_experiencia': experiencia,
        'remoto': remoto,
        'nivel_academico': nivel_academico,
        'postuladas': postuladas,
        'likes': likes,  # Nueva variable para likes
        'notificaciones': notificaciones,
    }

    return render(request, 'dashboard_empleado.html', context)

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

            messages.success(request, 'Oferta creada exitosamente. Los empleados serán notificados.')
            return redirect('dashboard_empresa')
    else:
        form = OfertaTrabajoForm()
    
    # Construir el diccionario de habilidades por industria para el JavaScript
    habilidades_por_industria = {
        industria: dict(form.HABILIDADES_POR_INDUSTRIA[industria]) 
        for industria in form.HABILIDADES_POR_INDUSTRIA
    }
    habilidades_blandas = dict(form.HABILIDADES_BLANDAS)

    return render(request, 'crear_oferta.html', {
        'form': form,
        'habilidades_por_industria_json': json.dumps(habilidades_por_industria),
        'habilidades_blandas_json': json.dumps(habilidades_blandas)
    })

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
    Notificacion.objects.filter(usuario=request.user).delete()

    return redirect('dashboard')

# Registro empleado
def registro_empleado(request):
    if request.method == 'POST':
        form = RegistroEmpleadoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.tipo_usuario = 'empleado'
                user.save()
                
                # Crear configuración de notificaciones por defecto
                ConfiguracionNotificaciones.objects.create(usuario=user)
                
                login(request, user)
                messages.success(request, "¡Registro exitoso! Ahora puedes comenzar a buscar ofertas de trabajo.")
                return redirect('dashboard')
            except IntegrityError:
                messages.error(request, "El nombre de usuario ya está en uso. Por favor, elige otro.")
    else:
        form = RegistroEmpleadoForm()
    return render(request, 'registro_empleado.html', {'form': form})

# Registro empresa + perfil
def registro_empresa(request):
    if request.method == 'POST':
        user_form = RegistroEmpresaForm(request.POST)
        perfil_form = PerfilEmpresaForm(request.POST)
        if user_form.is_valid() and perfil_form.is_valid():
            try:
                user = user_form.save(commit=False)
                user.tipo_usuario = 'empresa'
                user.save()

                perfil = perfil_form.save(commit=False)
                perfil.usuario = user
                perfil.save()
                
                # Crear configuración de notificaciones por defecto
                ConfiguracionNotificaciones.objects.create(usuario=user)

                login(request, user)
                messages.success(request, "¡Registro exitoso! Ahora puedes comenzar a publicar ofertas de trabajo.")
                return redirect('dashboard_empresa')
            except IntegrityError:
                messages.error(request, "El nombre de usuario ya está en uso. Por favor, elige otro.")
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

            # ✅ Redirección condicional según el tipo de usuario
            if user.tipo_usuario == 'empresa':
                return redirect('dashboard_empresa')
            else:
                return redirect('dashboard')  # solo empleados van al dashboard con preguntas

        return render(request, 'iniciar_sesion.html', {
            'error': 'Usuario o contraseña incorrectos'
        })
    
    # Por defecto, mostrar el formulario de login
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

# Vista extra para empresa
@login_required
def ver_ofertas_empresa(request):
    return dashboard_empresa(request)

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

@login_required
def toggle_like(request, oferta_id):
    if request.method == 'POST' and request.user.tipo_usuario == 'empleado':
        oferta = get_object_or_404(OfertaTrabajo, id=oferta_id)
        like, created = LikeOferta.objects.get_or_create(
            usuario=request.user,
            oferta=oferta
        )
        
        if not created:
            like.delete()
            return JsonResponse({'status': 'unliked', 'message': 'Like eliminado'})
        
        return JsonResponse({'status': 'liked', 'message': 'Like agregado'})
    return JsonResponse({'status': 'error', 'message': 'Solicitud inválida'}, status=400)

@login_required
def favoritos(request):
    if request.user.tipo_usuario != 'empleado':
        return redirect('dashboard')
    
    likes = LikeOferta.objects.filter(usuario=request.user).select_related('oferta')
    ofertas = [like.oferta for like in likes]
    
    return render(request, 'favoritos.html', {
        'ofertas': ofertas,
        'notificaciones': Notificacion.objects.filter(usuario=request.user)
    })

@login_required
def editar_oferta(request, oferta_id):
    # Verificar que el usuario sea empresa
    if request.user.tipo_usuario != 'empresa':
        messages.error(request, "No tienes permisos para editar ofertas.")
        return redirect('dashboard')
    
    # Obtener la oferta
    oferta = get_object_or_404(OfertaTrabajo, id=oferta_id, empresa=request.user)
    
    if request.method == 'POST':
        form = OfertaTrabajoForm(request.POST, instance=oferta)
        if form.is_valid():
            form.save()
            messages.success(request, "La oferta ha sido actualizada correctamente.")
            return redirect('ver_ofertas_empresa')
        else:
            # Si hay errores en el formulario, mostrar mensajes específicos
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en {field}: {error}")
    else:
        # Si las habilidades están almacenadas como JSON, convertirlas a lista para el formulario
        form = OfertaTrabajoForm(instance=oferta)
    
    # Construir el diccionario de habilidades por industria para el JavaScript
    habilidades_por_industria = {
        industria: dict(form.HABILIDADES_POR_INDUSTRIA[industria]) 
        for industria in form.HABILIDADES_POR_INDUSTRIA
    }
    habilidades_blandas = dict(form.HABILIDADES_BLANDAS)
    
    return render(request, 'editar_oferta.html', {
        'form': form,
        'oferta': oferta,
        'habilidades_por_industria_json': json.dumps(habilidades_por_industria),
        'habilidades_blandas_json': json.dumps(habilidades_blandas)
    })

@login_required
def preferencias_busqueda(request):
    if request.user.tipo_usuario != 'empresa':
        messages.error(request, "Solo empleadores pueden gestionar preferencias de búsqueda.")
        return redirect('dashboard')
    
    preferencias = PreferenciaBusqueda.objects.filter(usuario=request.user).order_by('-predeterminado')
    
    if request.method == 'POST':
        form = PreferenciaBusquedaForm(request.POST)
        if form.is_valid():
            preferencia = form.save(commit=False)
            preferencia.usuario = request.user
            preferencia.save()
            messages.success(request, "Preferencia de búsqueda guardada correctamente.")
            return redirect('preferencias_busqueda')
    else:
        form = PreferenciaBusquedaForm()
    
    return render(request, 'preferencias_busqueda.html', {
        'form': form,
        'preferencias': preferencias
    })

@login_required
def editar_preferencia(request, preferencia_id):
    if request.user.tipo_usuario != 'empresa':
        messages.error(request, "Solo empleadores pueden gestionar preferencias de búsqueda.")
        return redirect('dashboard')
    
    preferencia = get_object_or_404(PreferenciaBusqueda, id=preferencia_id, usuario=request.user)
    
    if request.method == 'POST':
        form = PreferenciaBusquedaForm(request.POST, instance=preferencia)
        if form.is_valid():
            form.save()
            messages.success(request, "Preferencia de búsqueda actualizada correctamente.")
            return redirect('preferencias_busqueda')
    else:
        form = PreferenciaBusquedaForm(instance=preferencia)
    
    return render(request, 'editar_preferencia.html', {
        'form': form,
        'preferencia': preferencia
    })

@login_required
def eliminar_preferencia(request, preferencia_id):
    if request.user.tipo_usuario != 'empresa':
        messages.error(request, "Solo empleadores pueden gestionar preferencias de búsqueda.")
        return redirect('dashboard')
    
    preferencia = get_object_or_404(PreferenciaBusqueda, id=preferencia_id, usuario=request.user)
    preferencia.delete()
    messages.success(request, "Preferencia de búsqueda eliminada correctamente.")
    return redirect('preferencias_busqueda')

@login_required
def aplicar_preferencia(request, preferencia_id):
    if request.user.tipo_usuario != 'empresa':
        return redirect('dashboard')
    
    preferencia = get_object_or_404(PreferenciaBusqueda, id=preferencia_id, usuario=request.user)
    
    # Construir la URL con los filtros de la preferencia
    params = {}
    if preferencia.nivel_experiencia:
        params['nivel_experiencia'] = preferencia.nivel_experiencia
    if preferencia.industria:
        params['industria'] = preferencia.industria
    if preferencia.ubicacion:
        params['ubicacion'] = preferencia.ubicacion
    if preferencia.remoto:
        params['remoto'] = preferencia.remoto
    if preferencia.nivel_academico:
        params['nivel_academico'] = preferencia.nivel_academico
    if preferencia.habilidades:
        params['habilidades'] = ','.join(preferencia.habilidades)
    
    # Construir la URL con los parámetros
    base_url = reverse('dashboard')
    query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
    url = f"{base_url}?{query_string}" if query_string else base_url
    
    return HttpResponseRedirect(url)

@login_required
def generar_reporte(request):
    if request.user.tipo_usuario != 'empresa':
        messages.error(request, "Solo empleadores pueden generar reportes.")
        return redirect('dashboard')
    
    # Parámetros del reporte
    tipo_reporte = request.GET.get('tipo', 'general')
    periodo = request.GET.get('periodo', '30')  # días
    
    try:
        periodo_dias = int(periodo)
    except ValueError:
        periodo_dias = 30
    
    fecha_inicio = timezone.now() - timedelta(days=periodo_dias)
    
    # Datos generales
    empresa = request.user
    ofertas = OfertaTrabajo.objects.filter(empresa=empresa)
    
    # Métricas
    total_ofertas = ofertas.count()
    ofertas_periodo = ofertas.filter(fecha_creacion__gte=fecha_inicio).count()
    
    postulaciones = Postulacion.objects.filter(oferta__empresa=empresa)
    total_postulaciones = postulaciones.count()
    postulaciones_periodo = postulaciones.filter(fecha_postulacion__gte=fecha_inicio).count()
    
    # Actividad por día
    actividad_diaria = postulaciones.filter(
        fecha_postulacion__gte=fecha_inicio
    ).annotate(
        dia=TruncDay('fecha_postulacion')
    ).values('dia').annotate(
        total=Count('id')
    ).order_by('dia')
    
    # Actividad por oferta
    actividad_por_oferta = postulaciones.filter(
        fecha_postulacion__gte=fecha_inicio
    ).values(
        'oferta__titulo'
    ).annotate(
        total=Count('id')
    ).order_by('-total')
    
    # Ofertas más populares (con más postulaciones)
    ofertas_populares = ofertas.annotate(
        num_postulaciones=Count('postulaciones')
    ).order_by('-num_postulaciones')[:5]
    
    context = {
        'empresa': empresa,
        'tipo_reporte': tipo_reporte,
        'periodo_dias': periodo_dias,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': timezone.now(),
        'total_ofertas': total_ofertas,
        'ofertas_periodo': ofertas_periodo,
        'total_postulaciones': total_postulaciones,
        'postulaciones_periodo': postulaciones_periodo,
        'actividad_diaria': actividad_diaria,
        'actividad_por_oferta': actividad_por_oferta,
        'ofertas_populares': ofertas_populares,
    }
    
    return render(request, 'reporte.html', context)

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

@login_required
def descargar_reporte_pdf(request):
    if request.user.tipo_usuario != 'empresa':
        messages.error(request, "Solo empleadores pueden generar reportes.")
        return redirect('dashboard')
    
    # Parámetros del reporte
    tipo_reporte = request.GET.get('tipo', 'general')
    periodo = request.GET.get('periodo', '30')  # días
    
    try:
        periodo_dias = int(periodo)
    except ValueError:
        periodo_dias = 30
    
    fecha_inicio = timezone.now() - timedelta(days=periodo_dias)
    
    # Datos generales
    empresa = request.user
    ofertas = OfertaTrabajo.objects.filter(empresa=empresa)
    
    # Métricas
    total_ofertas = ofertas.count()
    ofertas_periodo = ofertas.filter(fecha_creacion__gte=fecha_inicio).count()
    
    postulaciones = Postulacion.objects.filter(oferta__empresa=empresa)
    total_postulaciones = postulaciones.count()
    postulaciones_periodo = postulaciones.filter(fecha_postulacion__gte=fecha_inicio).count()
    
    # Actividad por día
    actividad_diaria = postulaciones.filter(
        fecha_postulacion__gte=fecha_inicio
    ).annotate(
        dia=TruncDay('fecha_postulacion')
    ).values('dia').annotate(
        total=Count('id')
    ).order_by('dia')
    
    # Actividad por oferta
    actividad_por_oferta = postulaciones.filter(
        fecha_postulacion__gte=fecha_inicio
    ).values(
        'oferta__titulo'
    ).annotate(
        total=Count('id')
    ).order_by('-total')
    
    # Ofertas más populares (con más postulaciones)
    ofertas_populares = ofertas.annotate(
        num_postulaciones=Count('postulaciones')
    ).order_by('-num_postulaciones')[:5]
    
    context = {
        'empresa': empresa,
        'tipo_reporte': tipo_reporte,
        'periodo_dias': periodo_dias,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': timezone.now(),
        'total_ofertas': total_ofertas,
        'ofertas_periodo': ofertas_periodo,
        'total_postulaciones': total_postulaciones,
        'postulaciones_periodo': postulaciones_periodo,
        'actividad_diaria': list(actividad_diaria),
        'actividad_por_oferta': list(actividad_por_oferta),
        'ofertas_populares': ofertas_populares,
    }
    
    # Renderizar a PDF
    pdf = render_to_pdf('reporte_pdf.html', context)
    
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"reporte_{tipo_reporte}_{timezone.now().strftime('%Y%m%d')}.pdf"
        content = f"attachment; filename={filename}"
        response['Content-Disposition'] = content
        return response
    
    return HttpResponse("Error al generar PDF", status=400)

# Editar perfil de empleado
@login_required
def editar_perfil_empleado(request):
    if request.user.tipo_usuario != 'empleado':
        messages.error(request, "No tienes permisos para editar este perfil.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = EditarPerfilEmpleadoForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Tu perfil ha sido actualizado correctamente.")
            return redirect('ver_perfil_empleado')
    else:
        form = EditarPerfilEmpleadoForm(instance=request.user)
    
    return render(request, 'editar_perfil_empleado.html', {
        'form': form
    })

# Ver perfil propio (empleado)
@login_required
def ver_perfil_empleado(request):
    if request.user.tipo_usuario != 'empleado':
        messages.error(request, "No tienes permisos para ver este perfil.")
        return redirect('dashboard')
    
    # Obtener las postulaciones del usuario
    postulaciones = Postulacion.objects.filter(usuario=request.user).select_related('oferta')
    
    return render(request, 'perfil_empleado.html', {
        'usuario': request.user,
        'postulaciones': postulaciones
    })

# Ver detalle de un postulante (para empresas)
@login_required
def ver_detalle_postulante(request, oferta_id, usuario_id):
    if request.user.tipo_usuario != 'empresa':
        messages.error(request, "No tienes permisos para ver este perfil.")
        return redirect('dashboard')
    
    # Verificar que la oferta pertenece a la empresa
    oferta = get_object_or_404(OfertaTrabajo, id=oferta_id, empresa=request.user)
    
    # Verificar que el usuario se ha postulado a esta oferta
    postulacion = get_object_or_404(Postulacion, oferta=oferta, usuario_id=usuario_id)
    
    # Obtener el usuario postulante
    postulante = postulacion.usuario
    
    # Obtener otras postulaciones del usuario
    otras_postulaciones = Postulacion.objects.filter(
        usuario=postulante, 
        oferta__empresa=request.user
    ).exclude(oferta_id=oferta_id).select_related('oferta')
    
    return render(request, 'detalle_postulante.html', {
        'postulante': postulante,
        'postulacion': postulacion,
        'oferta': oferta,
        'otras_postulaciones': otras_postulaciones
    })

# API para registrar cuando un usuario comienza a ver una oferta
@login_required
def iniciar_vista_oferta(request, oferta_id):
    if request.method == 'POST' and request.user.tipo_usuario == 'empleado':
        oferta = get_object_or_404(OfertaTrabajo, id=oferta_id)
        
        # Crear un registro de vista
        vista = VistaOferta.objects.create(
            usuario=request.user,
            oferta=oferta
        )
        
        return JsonResponse({
            'status': 'success', 
            'vista_id': vista.id,
            'timestamp': int(vista.timestamp_inicio.timestamp())
        })
    
    return JsonResponse({'status': 'error', 'message': 'Solicitud inválida'}, status=400)

# API para registrar cuando un usuario termina de ver una oferta
@login_required
def finalizar_vista_oferta(request, vista_id):
    if request.method == 'POST' and request.user.tipo_usuario == 'empleado':
        try:
            # Obtener la vista y verificar que pertenece al usuario
            vista = VistaOferta.objects.get(id=vista_id, usuario=request.user)
            
            # Calcular duración
            duracion = timezone.now() - vista.timestamp_inicio
            vista.duracion_segundos = int(duracion.total_seconds())
            vista.interaccion_completa = True
            vista.save()
            
            return JsonResponse({
                'status': 'success', 
                'duracion': vista.duracion_segundos
            })
        except VistaOferta.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Vista no encontrada'}, status=404)
    
    return JsonResponse({'status': 'error', 'message': 'Solicitud inválida'}, status=400)

@login_required
def obtener_recomendaciones(request):
    if request.user.tipo_usuario != 'empleado':
        return redirect('dashboard')
    
    # Obtener las recomendaciones personalizadas
    recomendaciones = generar_recomendaciones_usuario(request.user)
    
    # Obtener ofertas a las que ya se postuló y a las que dio like
    postuladas = Postulacion.objects.filter(usuario=request.user).values_list('oferta_id', flat=True)
    likes = LikeOferta.objects.filter(usuario=request.user).values_list('oferta_id', flat=True)
    
    return render(request, 'recomendaciones.html', {
        'ofertas': recomendaciones,
        'postuladas': postuladas,
        'likes': likes,
        'notificaciones': Notificacion.objects.filter(usuario=request.user)
    })

# Función que implementa el algoritmo de recomendación
def generar_recomendaciones_usuario(usuario, limit=10):
    """
    Genera recomendaciones personalizadas para un usuario basándose en:
    1. Sus interacciones (vistas, tiempo de visualización)
    2. Sus likes/favoritos
    3. Sus postulaciones previas
    4. Similaridad de habilidades y características de ofertas
    """
    # 1. Obtener todas las ofertas excepto a las que ya se postuló
    postulaciones_usuario = Postulacion.objects.filter(usuario=usuario).values_list('oferta_id', flat=True)
    ofertas_disponibles = OfertaTrabajo.objects.exclude(id__in=postulaciones_usuario)
    
    if not ofertas_disponibles.exists():
        return []
    
    # 2. Obtener patrones de interés basados en tiempo de visualización por industria, nivel experiencia, etc.
    vistas_usuario = VistaOferta.objects.filter(usuario=usuario)
    
    # Inicializar listas vacías en caso de que no haya vistas
    preferencia_industria = []
    preferencia_experiencia = []
    preferencia_remoto = []
    preferencia_nivel_academico = []
    
    # Calcular preferencias solo si el usuario tiene vistas registradas
    if vistas_usuario.exists():
        preferencia_industria = vistas_usuario.values('oferta__industria')\
            .annotate(total_tiempo=Sum('duracion_segundos'))\
            .order_by('-total_tiempo')
        
        preferencia_experiencia = vistas_usuario.values('oferta__nivel_experiencia')\
            .annotate(total_tiempo=Sum('duracion_segundos'))\
            .order_by('-total_tiempo')
        
        preferencia_remoto = vistas_usuario.values('oferta__remoto')\
            .annotate(total_tiempo=Sum('duracion_segundos'))\
            .order_by('-total_tiempo')
            
        preferencia_nivel_academico = vistas_usuario.values('oferta__nivel_academico')\
            .annotate(total_tiempo=Sum('duracion_segundos'))\
            .order_by('-total_tiempo')
    
    # 3. Obtener ofertas que le dió like
    favoritos_usuario = LikeOferta.objects.filter(usuario=usuario).values_list('oferta_id', flat=True)
    ofertas_con_like = OfertaTrabajo.objects.filter(id__in=favoritos_usuario)
    
    # 4. Asignar puntaje a cada oferta disponible
    recomendaciones = []
    
    for oferta in ofertas_disponibles:
        puntaje = 0
        
        # Puntaje base para todas las ofertas para asegurar algún resultado
        puntaje += random.uniform(0.1, 0.5)
        
        # Puntaje por industria basado en preferencias 
        for pref in preferencia_industria:
            if oferta.industria == pref['oferta__industria']:
                puntaje += min(10, pref['total_tiempo'] / 10)  # Máximo 10 puntos por industria
                break
        
        # Puntaje por nivel de experiencia
        for pref in preferencia_experiencia:
            if oferta.nivel_experiencia == pref['oferta__nivel_experiencia']:
                puntaje += min(5, pref['total_tiempo'] / 20)  # Máximo 5 puntos por nivel experiencia
                break
                
        # Puntaje por modalidad
        for pref in preferencia_remoto:
            if oferta.remoto == pref['oferta__remoto']:
                puntaje += min(5, pref['total_tiempo'] / 20)  # Máximo 5 puntos por modalidad
                break
                
        # Puntaje por nivel académico
        for pref in preferencia_nivel_academico:
            if oferta.nivel_academico == pref['oferta__nivel_academico']:
                puntaje += min(5, pref['total_tiempo'] / 20)  # Máximo 5 puntos por nivel académico
                break
        
        # Puntaje extra por ofertas similares a las que dio like
        for oferta_like in ofertas_con_like:
            if oferta_like.industria == oferta.industria:
                puntaje += 3  # Bonificación por industria similar
            if oferta_like.nivel_experiencia == oferta.nivel_experiencia:
                puntaje += 2  # Bonificación por nivel de experiencia similar
            
            # Verificar habilidades similares
            try:
                habilidades_oferta = set(oferta.habilidades)
                habilidades_like = set(oferta_like.habilidades)
                habilidades_comunes = habilidades_oferta.intersection(habilidades_like)
                puntaje += len(habilidades_comunes) * 0.5  # 0.5 puntos por cada habilidad común
            except (TypeError, AttributeError):
                # Manejar el caso de que habilidades no sea un conjunto iterable
                pass
        
        # Ofertas más recientes reciben un pequeño bonus
        dias_desde_publicacion = (timezone.now().date() - oferta.fecha_creacion.date()).days
        if dias_desde_publicacion < 15:  # Ofertas de menos de 15 días
            puntaje += max(0, (15 - dias_desde_publicacion) * 0.2)  # Hasta 3 puntos extra
        
        recomendaciones.append((oferta, puntaje))
    
    # Ordenar por puntaje y devolver las top N ofertas
    recomendaciones.sort(key=lambda x: x[1], reverse=True)
    
    # Asegurar que devolvemos al menos algunas recomendaciones, incluso si el puntaje es bajo
    result_ofertas = [rec[0] for rec in recomendaciones[:limit]]
    
    # Si no hay suficientes recomendaciones con puntajes significativos, completar con ofertas aleatorias
    if len(result_ofertas) < min(5, limit) and len(ofertas_disponibles) > len(result_ofertas):
        # Obtener IDs de las ofertas ya seleccionadas
        selected_ids = {oferta.id for oferta in result_ofertas}
        # Filtrar las ofertas disponibles que no están ya seleccionadas
        remaining_ofertas = [o for o in ofertas_disponibles if o.id not in selected_ids]
        # Seleccionar aleatoriamente hasta completar el mínimo
        random_ofertas = random.sample(remaining_ofertas, min(5 - len(result_ofertas), len(remaining_ofertas)))
        # Añadir a las recomendaciones
        result_ofertas.extend(random_ofertas)
    
    return result_ofertas