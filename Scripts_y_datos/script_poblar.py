import csv
import datetime

from django.db import transaction

from asistencia.models import Asistencia
from clases.models import Clase
from cursos.models import Curso
from usuarios.models import User


@transaction.atomic
def crear_cursos():
    curso_basico = Curso.objects.create(nombre="C++: Básico, FCFM", cant_clases=18)
    curso_avanzado = Curso.objects.create(nombre='C++: Avanzado, FCFM', cant_clases=18)


@transaction.atomic
def crear_usuarias(path):
    profes = []
    alumnas = []
    with open(path, 'r') as csvFile:
        reader = csv.reader(csvFile)
        headers = next(reader, None)
        for row in reader:
            print(row)
            nombre = row[0]
            apellido = row[1]
            usuaria = row[2]
            if row[3] == 'profesora':
                user = User.objects.create_user(username=usuaria, first_name=nombre, last_name=apellido,
                                                es_profesora=True, password='ninas20curso')
                profes.append(user)

            else:
                alumnas.append(
                    User.objects.create_user(username=usuaria, first_name=nombre, last_name=apellido,
                                             password='ninas20curso', es_profesora=True))
        csvFile.close()
    return {'profes': profes, 'alumnas': alumnas}


@transaction.atomic
def agregar_a_curso(curso, profes=[], alumnas=[]):
    for prof in profes:
        curso.profesoras.add(prof)

    for alumna in alumnas:
        curso.alumnas.add(alumna)


@transaction.atomic
def crear_clases(curso, path):
    with open(path, 'r') as csvFile:
        reader = csv.reader(csvFile)
        headers = next(reader, None)
        for row in reader:
            fecha_clase = row[1]
            date_clase = datetime.datetime.strptime(row[1], '%d/%m/%Y').date()
            Clase.objects.create(nombre=row[0], curso=curso, fecha_clase=date_clase)


@transaction.atomic
def crear_alumnas_dump():
    usuaria_alumna1 = User.objects.create_user(username="alumna1", first_name="Juana", last_name="Perez",
                                               password="contraseña123", es_alumna=True)

    usuaria_alumna2 = User.objects.create_user(username="alumna2", first_name="Claudia", last_name="Muñoz",
                                               password="contraseña123", es_alumna=True)

    usuaria_alumna3 = User.objects.create_user(username="alumna3", first_name="Claudia", last_name="Briones",
                                               password="contraseña123", es_alumna=True)

    usuaria_alumna4 = User.objects.create_user(username="alumna4", first_name="Claudia", last_name="Opazo",
                                               password="contraseña123", es_alumna=True)

    usuaria_alumna5 = User.objects.create_user(username="alumna5", first_name="Antonia", last_name="Quezada",
                                               password="contraseña123", es_alumna=True)

    usuaria_alumna6 = User.objects.create_user(username="alumna6", first_name="Fernanda", last_name="Macías",
                                               password="contraseña123", es_alumna=True)

    usuaria_alumna7 = User.objects.create_user(username="alumna7", first_name="Ignacia", last_name="Macías",
                                               password="contraseña123", es_alumna=True)

    usuaria_alumna8 = User.objects.create_user(username="alumna8", first_name="Ignacia", last_name="Labarca",
                                               password="contraseña123", es_alumna=True)

    usuaria_alumna9 = User.objects.create_user(username="alumna9", first_name="Karina", last_name="Rozas",
                                               password="contraseña123", es_alumna=True)

    usuaria_alumna10 = User.objects.create_user(username="alumna10", first_name="Florencia", last_name="Manríquez",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna11 = User.objects.create_user(username="alumna11", first_name="Antonia", last_name="Jimenez",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna12 = User.objects.create_user(username="alumna12", first_name="Constanza", last_name="Mora",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna13 = User.objects.create_user(username="alumna13", first_name="Rosario", last_name="González",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna14 = User.objects.create_user(username="alumna14", first_name="Lupe", last_name="Rojas",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna15 = User.objects.create_user(username="alumna15", first_name="Martina", last_name="Monsalves",
                                                password="contraseña123", es_alumna=True)



    alumnas_basico = [usuaria_alumna1, usuaria_alumna2, usuaria_alumna3, usuaria_alumna4, usuaria_alumna5,
                      usuaria_alumna6, usuaria_alumna7, usuaria_alumna8, usuaria_alumna9, usuaria_alumna10,
                      usuaria_alumna11, usuaria_alumna12, usuaria_alumna13, usuaria_alumna14, usuaria_alumna15]

    curso_basico = Curso.objects.get(nombre="C++: Básico, FCFM")

    for alumna in alumnas_basico:
        curso_basico.alumnas.add(alumna)



@transaction.atomic
def crear_alumnas(path, curso):
    with open(path, 'r') as csvFile:
        reader = csv.reader(csvFile)
        headers = next(reader, None)
        for row in reader:
            print(row[0])
            alumna= User.objects.create_user(username=row[0] + row[1] + '.' + row[2] + row[3],
                                          password='ninas20curso', es_alumna=True, first_name=row[0] + " " + row[1],
                                          last_name=row[2] + " " + row[3])
            curso.alumnas.add(alumna)
            curso.save()


@transaction.atomic
def crear_alumnas_asistencia(path, curso):
    with open(path, 'r') as csvFile:
        reader = csv.reader(csvFile)
        headers = next(reader, None)
        for row in reader:
            alumna, created = User.objects.get_or_create(username=row[0] + row[1] + '.' + row[2] + row[3],

                                                         es_alumna=True, first_name=row[0] + " " + row[1],
                                                         last_name=row[2] + " " + row[3])
            curso.alumnas.add(alumna)
            curso.save()
            for i in range(4, len(headers)):
                fecha = headers[i]
                date_clase = datetime.datetime.strptime(fecha, '%d/%m/%Y').date()
                print(date_clase)
                if date_clase != datetime.date(2020, 5, 2):
                    clase = Clase.objects.get(curso=curso, fecha_clase=date_clase)
                    print(row[i])
                    Asistencia.objects.create(alumna=alumna, clase=clase, asistio=True if row[i] == 'TRUE' else False)



crear_alumnas_dump()
