from .models import PreguntaPerfil, RespuestaPerfil

class PreguntasMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            respondidas = RespuestaPerfil.objects.filter(usuario=request.user).values_list('pregunta_id', flat=True)
            preguntas = PreguntaPerfil.objects.exclude(id__in=respondidas)

            # Evita mostrar preguntas con el mismo texto (duplicadas)
            preguntas_filtradas = []
            textos_vistos = set()
            for p in preguntas:
                if p.texto not in textos_vistos:
                    preguntas_filtradas.append(p)
                    textos_vistos.add(p.texto)

            request.preguntas_perfil = preguntas_filtradas[:3]
        else:
            request.preguntas_perfil = []

        return self.get_response(request)