import datetime

from django.db import transaction

from clases.models import Clase
from cursos.models import Curso
from usuarios.models import User


@transaction.atomic
def crear_cursos():
    curso_basico = Curso.objects.create(nombre="C++: Avanzado, FCFM", cant_clases=18)
    crear_usuarias(curso_basico)


def crear_usuarias(curso):
    profes = []
    alumnas = []
    profes.append(User.objects.get_or_create(username="valentina.urzua", es_profesora=True))

    profes.append(User.objects.get_or_create(username="jorge.pinto", es_profesora=True))
    profes.append(User.objects.get_or_create(username="pillippa.perez", es_profesora=True))

    alumnas.append(User.objects.create(username="alumnaA1", first_name="Juana", last_name="Perez",
                                            password="contraseña123", es_alumna=True))

    alumnas.append(User.objects.create(username="alumnaA2", first_name="Claudia", last_name="Muñoz",
                                            password="contraseña123", es_alumna=True))

    alumnas.append(User.objects.create(username="alumnaA3", first_name="Claudia", last_name="Briones",
                                            password="contraseña123", es_alumna=True))

    alumnas.append(User.objects.create(username="alumnaA4", first_name="Claudia", last_name="Opazo",
                                            password="contraseña123", es_alumna=True))

    for prof in profes:
        curso.profesoras.add(prof[0])

    for alu in alumnas:
        curso.alumnas.add(alu)

    curso.save()


def crear_clases(curso):
    if curso == Curso.objects.get(nombre="C++: Básico, FCFM"):
        clase_basico1 = Clase.objects.create(nombre="Bienvenida", curso=curso, fecha_clase=datetime.date(2020, 4, 4))
        clase_basico2 = Clase.objects.create(nombre="Algoritmos", curso=curso,
                                             fecha_clase=datetime.date(2020, 4, 11))
        clase_basico3 = Clase.objects.create(nombre="Variables", curso=curso, fecha_clase=datetime.date(2020, 4, 18))
        clase_basico4 = Clase.objects.create(nombre="Diagramas de flujo", curso=curso, fecha_clase=datetime.date(2020, 4, 25))
        clase_basico5 = Clase.objects.create(nombre="Condicionales", curso=curso, fecha_clase=datetime.date(2020, 5, 2))
    else:
        clase_medio1 = Clase.objects.create(nombre="Arreglos", curso=curso, fecha_clase=datetime.date(2020, 4, 4))
        clase_medio2 = Clase.objects.create(nombre="Variables", curso=cursoalu,
                                            fecha_clase=datetime.date(2020, 4, 11))
        clase_medio3 = Clase.objects.create(nombre="Listas Enlazadas", curso=curso,
                                            fecha_clase=datetime.date(2020, 4, 18))
        clase_medio4 = Clase.objects.create(nombre="Intro a la Programación Competitiva", curso=curso,
                                            fecha_clase=datetime.date(2020, 4, 25))
        clase_medio5 = Clase.objects.create(nombre="Intro a la Programación Competitiva 2", curso=curso,
                                            fecha_clase=datetime.date(2020, 5, 2))
