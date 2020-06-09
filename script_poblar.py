import csv
import datetime

from django.db import transaction

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

    usuaria_alumna16 = User.objects.create_user(username="alumna16", first_name="Belén", last_name="Acevedo",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna17 = User.objects.create_user(username="alumna17", first_name="Francisca", last_name="Riquelme",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna18 = User.objects.create_user(username="alumna18", first_name="Gabriela", last_name="Herrera",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna19 = User.objects.create_user(username="alumna19", first_name="Francisca", last_name="Fabres",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna20 = User.objects.create_user(username="alumna20", first_name="Bárbara", last_name="Fuentes",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna21 = User.objects.create_user(username="alumna21", first_name="Paula", last_name="Cifuentes",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna22 = User.objects.create_user(username="alumna22", first_name="Paulina", last_name="Lagos",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna23 = User.objects.create_user(username="alumna23", first_name="Alejandra", last_name="Rivas",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna24 = User.objects.create_user(username="alumna24", first_name="Mabel", last_name="Recabarren",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna25 = User.objects.create_user(username="alumna25", first_name="Teresa", last_name="Paredes",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna26 = User.objects.create_user(username="alumna26", first_name="Alicia", last_name="Cuadra",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna27 = User.objects.create_user(username="alumna27", first_name="Cecilia", last_name="Poblete",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna28 = User.objects.create_user(username="alumna28", first_name="Marta", last_name="Osorio",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna29 = User.objects.create_user(username="alumna29", first_name="Natalia", last_name="Arce",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna30 = User.objects.create_user(username="alumna30", first_name="Daniela", last_name="Medina",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna31 = User.objects.create_user(username="alumna31", first_name="Gabriela", last_name="Cuadra",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna32 = User.objects.create_user(username="alumna32", first_name="Luciana", last_name="Díaz",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna33 = User.objects.create_user(username="alumna33", first_name="Lucia", last_name="Cáceres",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna34 = User.objects.create_user(username="alumna34", first_name="Laura", last_name="Mierzo",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna35 = User.objects.create_user(username="alumna35", first_name="Scarlett", last_name="Suarez",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna36 = User.objects.create_user(username="alumna36", first_name="Catalina", last_name="Bravo",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna37 = User.objects.create_user(username="alumna37", first_name="Alejandra", last_name="Muñoz",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna38 = User.objects.create_user(username="alumna38", first_name="Josefa", last_name="Perez",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna39 = User.objects.create_user(username="alumna39", first_name="Josefina", last_name="Quiróz",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna40 = User.objects.create_user(username="alumna40", first_name="Monserrat", last_name="Martinez",
                                                password="contraseña123", es_alumna=True)

    alumnas_basico = [usuaria_alumna1, usuaria_alumna2, usuaria_alumna3, usuaria_alumna4, usuaria_alumna5,
                      usuaria_alumna6, usuaria_alumna7, usuaria_alumna8, usuaria_alumna9, usuaria_alumna10,
                      usuaria_alumna11, usuaria_alumna12, usuaria_alumna13, usuaria_alumna14, usuaria_alumna15,
                      usuaria_alumna16, usuaria_alumna17, usuaria_alumna18, usuaria_alumna19, usuaria_alumna20,
                      usuaria_alumna21, usuaria_alumna22, usuaria_alumna23, usuaria_alumna24, usuaria_alumna25,
                      usuaria_alumna26, usuaria_alumna27, usuaria_alumna28, usuaria_alumna29, usuaria_alumna30]

    alumnas_avanzado = [usuaria_alumna31, usuaria_alumna32, usuaria_alumna33, usuaria_alumna34, usuaria_alumna35,
                        usuaria_alumna36, usuaria_alumna37, usuaria_alumna38, usuaria_alumna39, usuaria_alumna40]

    curso_basico = Curso.objects.get(nombre="C++: Básico, FCFM")
    curso_avanzado = Curso.objects.get(nombre='C++: Avanzado, FCFM')

    for alumna in alumnas_basico:
        curso_basico.alumnas.add(alumna)

    for alumna in alumnas_avanzado:
        curso_avanzado.alumnas.add(alumna)


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

path = 'asistencia al 6_6 - Hoja 1.csv'
curso = Curso.objects.first()
crear_alumnas(path,curso)

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
