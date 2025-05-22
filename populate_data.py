import os
import django
import random
from datetime import timedelta
from django.utils import timezone

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'talentrackerproject.settings')
django.setup()

# Importar modelos después de configurar Django
from django.contrib.auth import get_user_model
from talentracker.models import (
    Usuario, PerfilEmpresa, OfertaTrabajo, Postulacion, 
    LikeOferta, VistaOferta, ConfiguracionNotificaciones
)

def populate():
    print("Poblando base de datos con datos de prueba...")
    
    # Eliminar datos existentes (opcional)
    #Usuario.objects.filter(email__contains='test').delete()
    
    # Crear empresas
    empresas = create_empresas()
    
    # Crear ofertas para cada empresa
    ofertas = create_ofertas(empresas)
    
    # Crear usuarios tipo empleado
    empleados = create_empleados()
    
    # Crear postulaciones y likes aleatorios
    create_interacciones(empleados, ofertas)
    
    print("Población de datos completada exitosamente!")

def create_empresas():
    empresas = []
    
    empresas_data = [
        {
            'username': 'tech_innovators',
            'email': 'reclutamiento@techinnovators.com',
            'password': 'tech2023',
            'first_name': 'Tech',
            'last_name': 'Innovators',
            'perfil': {
                'nombre_empresa': 'Tech Innovators SpA',
                'nit': '76.543.221-1',
                'descripcion': 'Empresa líder en desarrollo de software y soluciones tecnológicas.'
            }
        },
        {
            'username': 'salud_integral',
            'email': 'rrhh@saludintegral.com',
            'password': 'salud2023',
            'first_name': 'Salud',
            'last_name': 'Integral',
            'perfil': {
                'nombre_empresa': 'Salud Integral Ltda',
                'nit': '75.432.109-8',
                'descripcion': 'Red de clínicas y centros médicos con presencia nacional.'
            }
        },
        {
            'username': 'finanzas_globales',
            'email': 'talentos@finanzasglobales.com',
            'password': 'finanzas2023',
            'first_name': 'Finanzas',
            'last_name': 'Globales',
            'perfil': {
                'nombre_empresa': 'Finanzas Globales S.A.',
                'nit': '96.325.874-5',
                'descripcion': 'Empresa de servicios financieros y asesoría en inversiones.'
            }
        },
        {
            'username': 'edu_excellence',
            'email': 'contratacion@eduexcellence.com',
            'password': 'edu2023',
            'first_name': 'Educación',
            'last_name': 'Excellence',
            'perfil': {
                'nombre_empresa': 'Educación Excellence S.A.',
                'nit': '91.875.236-4',
                'descripcion': 'Red educativa con escuelas, institutos y centros de formación profesional.'
            }
        },
        {
            'username': 'service_solutions',
            'email': 'jobs@servicesolutions.com',
            'password': 'service2023',
            'first_name': 'Service',
            'last_name': 'Solutions',
            'perfil': {
                'nombre_empresa': 'Service Solutions Ltda',
                'nit': '88.777.666-3',
                'descripcion': 'Empresa proveedora de servicios generales y outsourcing.'
            }
        },
    ]
    
    for empresa_data in empresas_data:
        try:
            empresa, created = Usuario.objects.get_or_create(
                username=empresa_data['username'],
                defaults={
                    'email': empresa_data['email'],
                    'first_name': empresa_data['first_name'],
                    'last_name': empresa_data['last_name'],
                    'tipo_usuario': 'empresa',
                }
            )
            
            if created:
                empresa.set_password(empresa_data['password'])
                empresa.save()
            
            # Crear o actualizar perfil de empresa
            perfil, _ = PerfilEmpresa.objects.get_or_create(
                usuario=empresa,
                defaults=empresa_data['perfil']
            )
            
            # Crear configuración de notificaciones
            ConfiguracionNotificaciones.objects.get_or_create(usuario=empresa)
            
            empresas.append(empresa)
            print(f"Empresa creada: {empresa.username}")
        except Exception as e:
            print(f"Error al crear empresa {empresa_data['username']}: {str(e)}")
    
    return empresas

def create_ofertas(empresas):
    ofertas = []
    
    # Datos de ejemplo para cada industria
    ofertas_data = [
        # Tecnología
        {
            'titulo': 'Desarrollador Full Stack',
            'descripcion': 'Buscamos desarrollador full stack con experiencia en React, Django y PostgreSQL.',
            'industria': 'tecnologia',
            'ubicacion': 'Santiago',
            'nivel_experiencia': 'intermedio',
            'salario_estimado': 1800000.00,
            'remoto': 'hibrido',
            'nivel_academico': 'universitario',
            'habilidades': ['JavaScript', 'React', 'Python', 'Django', 'Git', 'Trabajo en equipo']
        },
        {
            'titulo': 'Ingeniero DevOps',
            'descripcion': 'Responsable de la infraestructura y automatización de despliegues en la nube.',
            'industria': 'tecnologia',
            'ubicacion': 'Santiago',
            'nivel_experiencia': 'senior',
            'salario_estimado': 2500000.00,
            'remoto': 'remoto',
            'nivel_academico': 'universitario',
            'habilidades': ['AWS', 'Docker', 'Kubernetes', 'CI/CD', 'Linux', 'Comunicación efectiva']
        },
        {
            'titulo': 'Diseñador UI/UX',
            'descripcion': 'Diseño de interfaces de usuario para aplicaciones web y móviles.',
            'industria': 'tecnologia',
            'ubicacion': 'Viña del Mar',
            'nivel_experiencia': 'junior',
            'salario_estimado': 1200000.00,
            'remoto': 'hibrido',
            'nivel_academico': 'tecnico',
            'habilidades': ['Figma', 'Adobe XD', 'HTML/CSS', 'Design Thinking', 'Creatividad']
        },
        
        # Salud
        {
            'titulo': 'Enfermero/a UCI',
            'descripcion': 'Atención a pacientes críticos en unidad de cuidados intensivos.',
            'industria': 'salud',
            'ubicacion': 'Concepción',
            'nivel_experiencia': 'senior',
            'salario_estimado': 1600000.00,
            'remoto': 'presencial',
            'nivel_academico': 'universitario',
            'habilidades': ['Cuidados intensivos', 'Manejo de emergencias', 'Técnicas de enfermería', 'Empatía']
        },
        {
            'titulo': 'Médico General',
            'descripcion': 'Atención de pacientes en consultorio general.',
            'industria': 'salud',
            'ubicacion': 'Santiago',
            'nivel_experiencia': 'intermedio',
            'salario_estimado': 2200000.00,
            'remoto': 'presencial',
            'nivel_academico': 'posgrado',
            'habilidades': ['Diagnóstico clínico', 'Atención primaria', 'Comunicación clara', 'Gestión del tiempo']
        },
        
        # Finanzas
        {
            'titulo': 'Analista Financiero',
            'descripcion': 'Análisis de datos financieros y elaboración de informes de gestión.',
            'industria': 'finanzas',
            'ubicacion': 'Santiago',
            'nivel_experiencia': 'intermedio',
            'salario_estimado': 1700000.00,
            'remoto': 'hibrido',
            'nivel_academico': 'universitario',
            'habilidades': ['Excel avanzado', 'Power BI', 'Análisis de datos', 'Contabilidad', 'Atención al detalle']
        },
        {
            'titulo': 'Asesor de Inversiones',
            'descripcion': 'Asesoramiento a clientes sobre productos de inversión y manejo de cartera.',
            'industria': 'finanzas',
            'ubicacion': 'Viña del Mar',
            'nivel_experiencia': 'senior',
            'salario_estimado': 2000000.00,
            'remoto': 'presencial',
            'nivel_academico': 'universitario',
            'habilidades': ['Mercado de valores', 'Análisis de riesgo', 'Atención al cliente', 'Negociación']
        },
        
        # Educación
        {
            'titulo': 'Profesor de Matemáticas',
            'descripcion': 'Impartir clases de matemáticas a nivel secundario.',
            'industria': 'educacion',
            'ubicacion': 'Valparaíso',
            'nivel_experiencia': 'intermedio',
            'salario_estimado': 1100000.00,
            'remoto': 'presencial',
            'nivel_academico': 'universitario',
            'habilidades': ['Pedagogía', 'Álgebra', 'Geometría', 'Evaluación educativa', 'Paciencia']
        },
        {
            'titulo': 'Coordinador Académico',
            'descripcion': 'Supervisión y coordinación del programa académico institucional.',
            'industria': 'educacion',
            'ubicacion': 'Santiago',
            'nivel_experiencia': 'senior',
            'salario_estimado': 1500000.00,
            'remoto': 'hibrido',
            'nivel_academico': 'posgrado',
            'habilidades': ['Gestión educativa', 'Planificación', 'Liderazgo', 'Resolución de conflictos']
        },
        
        # Servicios
        {
            'titulo': 'Supervisor de Operaciones',
            'descripcion': 'Coordinación de equipos de trabajo para servicios de limpieza industrial.',
            'industria': 'servicios',
            'ubicacion': 'Antofagasta',
            'nivel_experiencia': 'intermedio',
            'salario_estimado': 1300000.00,
            'remoto': 'presencial',
            'nivel_academico': 'tecnico',
            'habilidades': ['Supervisión', 'Logística', 'Gestión de personal', 'Trabajo bajo presión']
        },
        {
            'titulo': 'Ejecutivo de Atención al Cliente',
            'descripcion': 'Atención de consultas y resolución de problemas en servicio de call center.',
            'industria': 'servicios',
            'ubicacion': 'Santiago',
            'nivel_experiencia': 'junior',
            'salario_estimado': 850000.00,
            'remoto': 'remoto',
            'nivel_academico': 'secundaria',
            'habilidades': ['Comunicación verbal', 'Resolución de problemas', 'Empatía', 'Manejo de herramientas informáticas']
        },
    ]
    
    # Asignar ofertas a empresas según su industria principal
    industry_map = {
        'tecnologia': empresas[0],  # Tech Innovators
        'salud': empresas[1],       # Salud Integral
        'finanzas': empresas[2],    # Finanzas Globales
        'educacion': empresas[3],   # Educación Excellence
        'servicios': empresas[4],   # Service Solutions
    }
    
    for oferta_data in ofertas_data:
        try:
            # Asignar a la empresa correspondiente o seleccionar una aleatoria
            empresa = industry_map.get(oferta_data['industria'], random.choice(empresas))
            
            # Crear oferta
            oferta, created = OfertaTrabajo.objects.get_or_create(
                titulo=oferta_data['titulo'],
                empresa=empresa,
                defaults={
                    'descripcion': oferta_data['descripcion'],
                    'industria': oferta_data['industria'],
                    'ubicacion': oferta_data['ubicacion'],
                    'nivel_experiencia': oferta_data['nivel_experiencia'],
                    'salario_estimado': oferta_data['salario_estimado'],
                    'remoto': oferta_data['remoto'],
                    'nivel_academico': oferta_data['nivel_academico'],
                    'habilidades': oferta_data['habilidades'],
                }
            )
            
            if created:
                # Ajustar fecha de creación para que algunas ofertas sean más antiguas
                oferta.fecha_creacion = timezone.now() - timedelta(days=random.randint(0, 60))
                oferta.save()
                
            ofertas.append(oferta)
            print(f"Oferta creada: {oferta.titulo} - {empresa.username}")
        except Exception as e:
            print(f"Error al crear oferta {oferta_data['titulo']}: {str(e)}")
    
    # Crear algunas ofertas adicionales con datos aleatorios para diversificar
    industrias = ['tecnologia', 'salud', 'finanzas', 'educacion', 'servicios']
    niveles = ['junior', 'intermedio', 'senior']
    remoto_opciones = ['presencial', 'remoto', 'hibrido']
    nivel_academico_opciones = ['secundaria', 'tecnico', 'universitario', 'posgrado']
    ubicaciones = ['Santiago', 'Concepción', 'Valparaíso', 'Antofagasta', 'Puerto Montt', 'La Serena', 'Temuco']
    
    for i in range(10):
        try:
            industria = random.choice(industrias)
            empresa = industry_map.get(industria, random.choice(empresas))
            
            oferta = OfertaTrabajo.objects.create(
                empresa=empresa,
                titulo=f"Puesto random {i+1} - {industria}",
                descripcion=f"Esta es una descripción generada automáticamente para la oferta {i+1}.",
                industria=industria,
                ubicacion=random.choice(ubicaciones),
                nivel_experiencia=random.choice(niveles),
                salario_estimado=random.randint(500000, 3000000),
                remoto=random.choice(remoto_opciones),
                nivel_academico=random.choice(nivel_academico_opciones),
                habilidades=["Habilidad 1", "Habilidad 2", "Habilidad 3"],
                fecha_creacion=timezone.now() - timedelta(days=random.randint(0, 30))
            )
            
            ofertas.append(oferta)
            print(f"Oferta adicional creada: {oferta.titulo}")
        except Exception as e:
            print(f"Error al crear oferta adicional {i+1}: {str(e)}")
    
    return ofertas

def create_empleados():
    empleados = []
    
    empleados_data = [
        {
            'username': 'juan_perez',
            'email': 'juan.perez@example.com',
            'password': 'juan2023',
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'telefono': '+56 9 1234 5678',
            'fecha_nacimiento': '1990-01-15',
            'genero': 'M',
            'biografia': 'Ingeniero en informática con experiencia en desarrollo web.'
        },
        {
            'username': 'maria_rodriguez',
            'email': 'maria.rodriguez@example.com',
            'password': 'maria2023',
            'first_name': 'María',
            'last_name': 'Rodríguez',
            'telefono': '+56 9 8765 4321',
            'fecha_nacimiento': '1992-05-20',
            'genero': 'F',
            'biografia': 'Enfermera profesional especializada en cuidados intensivos.'
        },
        {
            'username': 'carlos_gonzalez',
            'email': 'carlos.gonzalez@example.com',
            'password': 'carlos2023',
            'first_name': 'Carlos',
            'last_name': 'González',
            'telefono': '+56 9 5555 1234',
            'fecha_nacimiento': '1988-09-10',
            'genero': 'M',
            'biografia': 'Contador auditor con 8 años de experiencia en el sector financiero.'
        },
        {
            'username': 'ana_martinez',
            'email': 'ana.martinez@example.com',
            'password': 'ana2023',
            'first_name': 'Ana',
            'last_name': 'Martínez',
            'telefono': '+56 9 4444 5555',
            'fecha_nacimiento': '1995-03-25',
            'genero': 'F',
            'biografia': 'Diseñadora UX/UI apasionada por crear experiencias digitales.'
        },
        {
            'username': 'pedro_sanchez',
            'email': 'pedro.sanchez@example.com',
            'password': 'pedro2023',
            'first_name': 'Pedro',
            'last_name': 'Sánchez',
            'telefono': '+56 9 7777 8888',
            'fecha_nacimiento': '1985-11-05',
            'genero': 'M',
            'biografia': 'Profesor de matemáticas con experiencia en educación secundaria y superior.'
        },
        {
            'username': 'laura_diaz',
            'email': 'laura.diaz@example.com',
            'password': 'laura2023',
            'first_name': 'Laura',
            'last_name': 'Díaz',
            'telefono': '+56 9 3333 2222',
            'fecha_nacimiento': '1993-07-18',
            'genero': 'F',
            'biografia': 'Ingeniera comercial especializada en análisis de datos y finanzas.'
        },
        {
            'username': 'diego_lopez',
            'email': 'diego.lopez@example.com',
            'password': 'diego2023',
            'first_name': 'Diego',
            'last_name': 'López',
            'telefono': '+56 9 6666 7777',
            'fecha_nacimiento': '1991-12-30',
            'genero': 'M',
            'biografia': 'Desarrollador backend con conocimientos en Python, Java y bases de datos.'
        },
        {
            'username': 'sofia_torres',
            'email': 'sofia.torres@example.com',
            'password': 'sofia2023',
            'first_name': 'Sofía',
            'last_name': 'Torres',
            'telefono': '+56 9 9999 0000',
            'fecha_nacimiento': '1994-04-12',
            'genero': 'F',
            'biografia': 'Psicóloga clínica con enfoque en terapia cognitivo-conductual.'
        },
        {
            'username': 'javier_navarro',
            'email': 'javier.navarro@example.com',
            'password': 'javier2023',
            'first_name': 'Javier',
            'last_name': 'Navarro',
            'telefono': '+56 9 2222 3333',
            'fecha_nacimiento': '1987-08-22',
            'genero': 'M',
            'biografia': 'Técnico en administración con experiencia en logística y operaciones.'
        },
        {
            'username': 'carolina_munoz',
            'email': 'carolina.munoz@example.com',
            'password': 'carolina2023',
            'first_name': 'Carolina',
            'last_name': 'Muñoz',
            'telefono': '+56 9 8888 1111',
            'fecha_nacimiento': '1996-02-08',
            'genero': 'F',
            'biografia': 'Periodista especializada en medios digitales y redes sociales.'
        }
    ]
    
    for empleado_data in empleados_data:
        try:
            fecha_nacimiento = None
            if 'fecha_nacimiento' in empleado_data:
                from datetime import datetime
                fecha_nacimiento = datetime.strptime(empleado_data['fecha_nacimiento'], '%Y-%m-%d').date()
            
            empleado, created = Usuario.objects.get_or_create(
                username=empleado_data['username'],
                defaults={
                    'email': empleado_data['email'],
                    'first_name': empleado_data['first_name'],
                    'last_name': empleado_data['last_name'],
                    'tipo_usuario': 'empleado',
                    'telefono': empleado_data.get('telefono'),
                    'fecha_nacimiento': fecha_nacimiento,
                    'genero': empleado_data.get('genero'),
                    'biografia': empleado_data.get('biografia'),
                }
            )
            
            if created:
                empleado.set_password(empleado_data['password'])
                empleado.save()
            
            # Crear configuración de notificaciones
            ConfiguracionNotificaciones.objects.get_or_create(usuario=empleado)
            
            empleados.append(empleado)
            print(f"Empleado creado: {empleado.username}")
        except Exception as e:
            print(f"Error al crear empleado {empleado_data['username']}: {str(e)}")
    
    return empleados

def create_interacciones(empleados, ofertas):
    # Postulaciones: cada empleado postula a 2-5 ofertas
    for empleado in empleados:
        # Seleccionar ofertas aleatorias para este empleado
        num_postulaciones = random.randint(2, 5)
        ofertas_seleccionadas = random.sample(ofertas, num_postulaciones)
        
        for oferta in ofertas_seleccionadas:
            try:
                postulacion, created = Postulacion.objects.get_or_create(
                    usuario=empleado,
                    oferta=oferta
                )
                if created:
                    # Fecha de postulación aleatoria en el último mes
                    dias_atras = random.randint(0, 30)
                    postulacion.fecha_postulacion = timezone.now() - timedelta(days=dias_atras)
                    postulacion.save()
                    print(f"Postulación creada: {empleado.username} -> {oferta.titulo}")
            except Exception as e:
                print(f"Error al crear postulación para {empleado.username} a {oferta.titulo}: {str(e)}")
    
    # Likes: cada empleado da like a 3-8 ofertas (excluyendo a las que ya se postuló)
    for empleado in empleados:
        # Obtener ofertas a las que ya se postuló
        postulaciones = Postulacion.objects.filter(usuario=empleado)
        ofertas_postuladas = [p.oferta for p in postulaciones]
        
        # Ofertas disponibles (excluyendo a las que ya se postuló)
        ofertas_disponibles = [o for o in ofertas if o not in ofertas_postuladas]
        
        # Seleccionar ofertas aleatorias para dar like
        num_likes = min(random.randint(3, 8), len(ofertas_disponibles))
        if num_likes > 0:
            ofertas_para_like = random.sample(ofertas_disponibles, num_likes)
            
            for oferta in ofertas_para_like:
                try:
                    like, created = LikeOferta.objects.get_or_create(
                        usuario=empleado,
                        oferta=oferta
                    )
                    if created:
                        print(f"Like creado: {empleado.username} -> {oferta.titulo}")
                except Exception as e:
                    print(f"Error al crear like para {empleado.username} a {oferta.titulo}: {str(e)}")
    
    # Vistas: crear registros de vistas para las ofertas (incluyendo tiempo de visualización)
    for empleado in empleados:
        # Seleccionar ofertas aleatorias para ver (puede incluir ofertas a las que ya se postuló)
        num_vistas = random.randint(5, 15)
        ofertas_para_ver = random.sample(ofertas, min(num_vistas, len(ofertas)))
        
        for oferta in ofertas_para_ver:
            try:
                # Tiempo de visualización aleatorio entre 10 y 300 segundos
                duracion = random.randint(10, 300)
                
                vista = VistaOferta.objects.create(
                    usuario=empleado,
                    oferta=oferta,
                    duracion_segundos=duracion,
                    interaccion_completa=random.choice([True, False])
                )
                
                # Fecha de vista aleatoria en el último mes
                dias_atras = random.randint(0, 30)
                vista.timestamp_inicio = timezone.now() - timedelta(days=dias_atras)
                vista.save()
                
                print(f"Vista creada: {empleado.username} vio {oferta.titulo} por {duracion}s")
            except Exception as e:
                print(f"Error al crear vista para {empleado.username} a {oferta.titulo}: {str(e)}")

if __name__ == '__main__':
    populate() 