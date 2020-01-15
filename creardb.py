from usuarios.models import *
from cursos.models import Curso
from asistencia.models import Asistencia
from clases.models import Clase
"""
curso_basico = Curso.objects.create(nombre="C++: Básico")
curso_avanzado = Curso.objects.create(nombre="C++: Avanzado")
curso_uandes = Curso.objects.create(nombre="Programación Uandes")



usuaria_profesora = User.objects.create_user(username="profesora", password="contraseña123",es_profesora=True)

usuaria_profesora2 = User.objects.create_user(username="profesora2", password="contraseña123",es_profesora=True)
usuaria_voluntaria = User.objects.create_user(username="voluntaria", password="contraseña123",es_voluntaria=True)

usuaria_voluntaria2 = User.objects.create_user(username="voluntaria2", password="contraseña123",es_voluntaria=True)

usuaria_voluntaria3 = User.objects.create_user(username="voluntaria3", password="contraseña123",es_voluntaria=True)

curso_basico.profesoras.add(usuaria_profesora2)
curso_basico.voluntarias.add(usuaria_voluntaria2)
curso_basico.voluntarias.add(usuaria_voluntaria3)


curso_avanzado.profesoras.add(usuaria_profesora2)
curso_avanzado.voluntarias.add(usuaria_voluntaria2)
curso_avanzado.voluntarias.add(usuaria_voluntaria3)


curso_uandes.profesoras.add(usuaria_profesora)
curso_uandes.voluntarias.add(usuaria_voluntaria)

"""

usuaria_alumna1 = User.objects.create_user(username="alumna1", first_name="Juana", last_name="Perez", password="contraseña123", es_alumna=True)

usuaria_alumna2 = User.objects.create_user(username="alumna2", first_name="Claudia", last_name="Muñoz", password="contraseña123", es_alumna=True)

usuaria_alumna3 = User.objects.create_user(username="alumna3", first_name="Claudia", last_name="Briones", password="contraseña123", es_alumna=True)

usuaria_alumna4 = User.objects.create_user(username="alumna4", first_name="Claudia", last_name="Opazo", password="contraseña123", es_alumna=True)

usuaria_alumna5 = User.objects.create_user(username="alumna5", first_name="Antonia", last_name="Quezada", password="contraseña123", es_alumna=True)

curso_basico = Curso.objects.create(nombre="C++: Básico")
curso_basico.profesoras.add(usuaria_profesora1)
curso_basico.voluntarias.add(usuaria_voluntaria1)
curso_basico.voluntarias.add(usuaria_voluntaria2)
curso_basico.alumnas.add(usuaria_alumna1)
curso_basico.alumnas.add(usuaria_alumna2)
curso_basico.alumnas.add(usuaria_alumna3)
curso_basico.alumnas.add(usuaria_alumna4)
curso_basico.alumnas.add(usuaria_alumna5)


curso_avanzado = Curso.objects.create(nombre="C++: Avanzado")
curso_avanzado.profesoras.add(usuaria_profesora2)
curso_avanzado.voluntarias.add(usuaria_voluntaria2)
curso_basico.alumnas.add(usuaria_alumna2)
curso_basico.alumnas.add(usuaria_alumna3)
curso_basico.alumnas.add(usuaria_alumna4)


## ASISTENCIA

clase_basico1 = Clase.objects.create(nombre="Clase 1: Ciclos for", curso=curso_basico)
clase_basico2 = Clase.objects.create(nombre="Clase 2: Ciclos while", curso=curso_basico)

## basico1 : alumna1, alumna3, alumna4, alumna2
## basico2 : alumna2, alumna4

usuaria_alumna1 = User.objects.filter(username="alumna1")[0]

Asistencia.objects.create(alumna=usuaria_alumna1, clase=clase_basico1, author=usuaria_profesora, asistio=True)

Asistencia.objects.create(alumna=usuaria_alumna2, clase=clase_basico1, author=usuaria_profesora, asistio=True)

Asistencia.objects.create(alumna=usuaria_alumna3, clase=clase_basico1, author=usuaria_profesora, asistio=True)

Asistencia.objects.create(alumna=usuaria_alumna4, clase=clase_basico1, author=usuaria_profesora, asistio=True)

Asistencia.objects.create(alumna=usuaria_alumna5, clase=clase_basico1, author=usuaria_profesora, asistio=True)


Asistencia.objects.create(alumna=usuaria_alumna1, clase=clase_basico2, author=usuaria_profesora, asistio=False)

Asistencia.objects.create(alumna=usuaria_alumna2, clase=clase_basico2, author=usuaria_profesora, asistio=True)

Asistencia.objects.create(alumna=usuaria_alumna3, clase=clase_basico2, author=usuaria_profesora, asistio=False)

Asistencia.objects.create(alumna=usuaria_alumna4, clase=clase_basico2, author=usuaria_profesora, asistio=True)

Asistencia.objects.create(alumna=usuaria_alumna5, clase=clase_basico2, author=usuaria_profesora, asistio=False)