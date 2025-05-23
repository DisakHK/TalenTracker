import os
import django
import random
from datetime import datetime, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'talentrackerproject.settings')
django.setup()

from django.contrib.auth import get_user_model
from talentracker.models import PerfilProfesional, OfertaTrabajo, LikeOferta, Postulacion

# Obtener el modelo de Usuario
Usuario = get_user_model()

# Definir las industrias y sus perfiles correspondientes
PERFILES_POR_INDUSTRIA = {
    'tecnologia': {
        'habilidades': ['Python', 'JavaScript', 'React', 'Node.js', 'SQL', 'Git', 'DevOps'],
        'nivel_experiencia': 'intermedio',
        'ubicacion': 'Santiago',
        'preferencia_modalidad': 'hibrido',
        'nivel_academico': 'universitario'
    },
    'educacion': {
        'habilidades': ['Pedagogía', 'Gestión educativa', 'Evaluación', 'Planificación', 'Trabajo en equipo'],
        'nivel_experiencia': 'senior',
        'ubicacion': 'Valparaíso',
        'preferencia_modalidad': 'presencial',
        'nivel_academico': 'posgrado'
    },
    'finanzas': {
        'habilidades': ['Análisis financiero', 'Excel avanzado', 'SAP', 'Contabilidad', 'Gestión de riesgos'],
        'nivel_experiencia': 'senior',
        'ubicacion': 'Santiago',
        'preferencia_modalidad': 'presencial',
        'nivel_academico': 'universitario'
    },
    'salud': {
        'habilidades': ['Atención al paciente', 'Gestión clínica', 'Historia clínica', 'Primeros auxilios'],
        'nivel_experiencia': 'intermedio',
        'ubicacion': 'Concepción',
        'preferencia_modalidad': 'presencial',
        'nivel_academico': 'universitario'
    },
    'servicios': {
        'habilidades': ['Atención al cliente', 'Ventas', 'CRM', 'Negociación', 'Resolución de problemas'],
        'nivel_experiencia': 'junior',
        'ubicacion': 'Santiago',
        'preferencia_modalidad': 'hibrido',
        'nivel_academico': 'tecnico'
    }
}

def crear_usuario_enfocado(industria, numero):
    """Crea un usuario enfocado en una industria específica"""
    username = f"empleado_{industria}_{numero}"
    email = f"{username}@example.com"
    perfil = PERFILES_POR_INDUSTRIA[industria]
    
    # Eliminar usuario si ya existe
    Usuario.objects.filter(username=username).delete()
    
    # Crear usuario
    usuario = Usuario.objects.create_user(
        username=username,
        email=email,
        password='empleado2023',
        tipo_usuario='empleado',
        first_name=f"Empleado {industria.capitalize()}",
        last_name=f"Apellido {numero}",
        fecha_nacimiento=datetime.now() - timedelta(days=365*25),
        genero='O'
    )
    
    # Crear perfil profesional
    PerfilProfesional.objects.create(
        usuario=usuario,
        habilidades=perfil['habilidades'],
        nivel_experiencia=perfil['nivel_experiencia'],
        ubicacion=perfil['ubicacion'],
        preferencia_modalidad=perfil['preferencia_modalidad'],
        nivel_academico=perfil['nivel_academico']
    )
    
    # Dar likes y postular a ofertas de la industria
    ofertas = OfertaTrabajo.objects.filter(industria=industria)
    for oferta in ofertas:
        # 70% de probabilidad de dar like
        if random.random() < 0.7:
            LikeOferta.objects.create(
                usuario=usuario,
                oferta=oferta
            )
        
        # 50% de probabilidad de postular
        if random.random() < 0.5:
            Postulacion.objects.create(
                usuario=usuario,
                oferta=oferta
            )
    
    return usuario

def main():
    # Distribuir 10 usuarios entre las industrias
    industrias = list(PERFILES_POR_INDUSTRIA.keys())
    usuarios_por_industria = {industria: 2 for industria in industrias}
    
    print("Creando usuarios enfocados por industria...")
    for industria, cantidad in usuarios_por_industria.items():
        for i in range(cantidad):
            usuario = crear_usuario_enfocado(industria, i+1)
            print(f"Usuario creado: {usuario.username}")
    
    print("\nProceso completado!")
    print("Usuarios creados por industria:")
    for industria in industrias:
        count = Usuario.objects.filter(username__startswith=f"empleado_{industria}").count()
        print(f"- {industria.capitalize()}: {count} usuarios")

if __name__ == '__main__':
    main() 