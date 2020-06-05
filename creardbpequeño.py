import datetime
import random

from django.db import transaction

from usuarios.models import *
from cursos.models import Curso
from asistencia.models import Asistencia
from clases.models import Clase


## CURSOS
@transaction.atomic
def poblar_db():
    # guardado en la bdd
    curso_basico = Curso.objects.create(nombre="C++: Básico, FCFM", cant_clases=8)
    curso_medio = Curso.objects.create(nombre="C++: Medio, FCFM", cant_clases=8)
    curso_basico_umayor = Curso.objects.create(nombre="C++: Básico, UMayor", cant_clases=8)
    curso_medio_umayor = Curso.objects.create(nombre="C++: Medio, UMayor", cant_clases=8)

    ## PROFESORAS

    # guardado en la bdd
    usuaria_profesora = User.objects.create_user(username="profesora", password="contraseña123", es_profesora=True)
    usuaria_profesora2 = User.objects.create_user(username="profesora2", password="contraseña123", es_profesora=True)

    # nuevo
    usuaria_profesora3 = User.objects.create_user(username="profesora3", password="contraseña123", es_profesora=True)
    usuaria_profesora4 = User.objects.create_user(username="profesora4", password="contraseña123", es_profesora=True)
    usuaria_profesora5 = User.objects.create_user(username="profesora5", password="contraseña123", es_profesora=True)
    usuaria_profesora6 = User.objects.create_user(username="profesora6", password="contraseña123", es_profesora=True)
    usuaria_profesora7 = User.objects.create_user(username="profesora7", password="contraseña123", es_profesora=True)
    usuaria_profesora8 = User.objects.create_user(username="profesora8", password="contraseña123", es_profesora=True)

    ## VOLUNTARIAS

    # guardado en la bdd
    usuaria_voluntaria = User.objects.create_user(username="voluntaria", password="contraseña123", es_voluntaria=True)
    usuaria_voluntaria2 = User.objects.create_user(username="voluntaria2", password="contraseña123", es_voluntaria=True)
    usuaria_voluntaria3 = User.objects.create_user(username="voluntaria3", password="contraseña123", es_voluntaria=True)
    # nuevo
    usuaria_voluntaria4 = User.objects.create_user(username="voluntaria4", password="contraseña123", es_voluntaria=True)
    usuaria_voluntaria5 = User.objects.create_user(username="voluntaria5", password="contraseña123", es_voluntaria=True)
    usuaria_voluntaria6 = User.objects.create_user(username="voluntaria6", password="contraseña123", es_voluntaria=True)
    usuaria_voluntaria7 = User.objects.create_user(username="voluntaria7", password="contraseña123", es_voluntaria=True)
    usuaria_voluntaria8 = User.objects.create_user(username="voluntaria8", password="contraseña123", es_voluntaria=True)
    usuaria_voluntaria9 = User.objects.create_user(username="voluntaria9", password="contraseña123", es_voluntaria=True)

    ## RELACIONES USUARIAS CURSOS

    # ya esta en la bdd
    curso_basico.profesoras.add(usuaria_profesora)
    curso_medio.profesoras.add(usuaria_profesora2)

    # nuevo
    curso_basico_umayor.profesoras.add(usuaria_profesora6)
    curso_medio_umayor.profesoras.add(usuaria_profesora7)

    # ya esta en la bdd
    curso_basico.voluntarias.add(usuaria_voluntaria)
    curso_basico.voluntarias.add(usuaria_voluntaria2)

    curso_medio.voluntarias.add(usuaria_voluntaria2)
    curso_medio.voluntarias.add(usuaria_voluntaria3)

    # nuevo
    curso_basico_umayor.voluntarias.add(usuaria_voluntaria6)
    curso_basico_umayor.voluntarias.add(usuaria_voluntaria7)

    curso_medio_umayor.voluntarias.add(usuaria_voluntaria7)
    curso_medio_umayor.voluntarias.add(usuaria_voluntaria8)

    ## ya esta en la bdd
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

    usuaria_alumna41 = User.objects.create_user(username="alumna41", first_name="Valentina", last_name="Ruiz",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna42 = User.objects.create_user(username="alumna42", first_name="Margarita", last_name="Elfernan",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna43 = User.objects.create_user(username="alumna43", first_name="Javiera", last_name="Ramos",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna44 = User.objects.create_user(username="alumna44", first_name="María José", last_name="Del Campo",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna45 = User.objects.create_user(username="alumna45", first_name="Kiara", last_name="De la Maza",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna46 = User.objects.create_user(username="alumna46", first_name="Karen", last_name="James",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna47 = User.objects.create_user(username="alumna47", first_name="Sofía", last_name="Toledo",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna48 = User.objects.create_user(username="alumna48", first_name="Agustina", last_name="Timana",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna49 = User.objects.create_user(username="alumna49", first_name="Dominga", last_name="Espinoza",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna50 = User.objects.create_user(username="alumna50", first_name="Asunción", last_name="Gómez",
                                                password="contraseña123", es_alumna=True)

    ## por agregar a la bdd

    usuaria_alumna51 = User.objects.create_user(username="alumna51", first_name="Fernanda", last_name="Macías",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna52 = User.objects.create_user(username="alumna52", first_name="Ignacia", last_name="Macías",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna53 = User.objects.create_user(username="alumna53", first_name="Ignacia", last_name="Labarca",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna54 = User.objects.create_user(username="alumna54", first_name="Karina", last_name="Rozas",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna55 = User.objects.create_user(username="alumna55", first_name="Florencia", last_name="Manríquez",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna56 = User.objects.create_user(username="alumna56", first_name="Antonia", last_name="Jimenez",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna57 = User.objects.create_user(username="alumna57", first_name="Constanza", last_name="Mora",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna58 = User.objects.create_user(username="alumna58", first_name="Rosario", last_name="González",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna59 = User.objects.create_user(username="alumna59", first_name="Lupe", last_name="Rojas",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna60 = User.objects.create_user(username="alumna60", first_name="Martina", last_name="Monsalves",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna61 = User.objects.create_user(username="alumna61", first_name="Belén", last_name="Acevedo",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna62 = User.objects.create_user(username="alumna62", first_name="Francisca", last_name="Riquelme",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna63 = User.objects.create_user(username="alumna63", first_name="Gabriela", last_name="Herrera",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna64 = User.objects.create_user(username="alumna64", first_name="Francisca", last_name="Fabres",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna65 = User.objects.create_user(username="alumna65", first_name="Bárbara", last_name="Fuentes",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna66 = User.objects.create_user(username="alumna66", first_name="Paula", last_name="Cifuentes",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna67 = User.objects.create_user(username="alumna67", first_name="Paulina", last_name="Lagos",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna68 = User.objects.create_user(username="alumna68", first_name="Alejandra", last_name="Rivas",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna69 = User.objects.create_user(username="alumna69", first_name="Mabel", last_name="Recabarren",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna70 = User.objects.create_user(username="alumna70", first_name="Teresa", last_name="Paredes",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna71 = User.objects.create_user(username="alumna71", first_name="Alicia", last_name="Cuadra",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna72 = User.objects.create_user(username="alumna72", first_name="Cecilia", last_name="Poblete",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna73 = User.objects.create_user(username="alumna73", first_name="Marta", last_name="Osorio",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna74 = User.objects.create_user(username="alumna74", first_name="Natalia", last_name="Arce",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna75 = User.objects.create_user(username="alumna75", first_name="Daniela", last_name="Medina",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna76 = User.objects.create_user(username="alumna76", first_name="Gabriela", last_name="Cuadra",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna77 = User.objects.create_user(username="alumna77", first_name="Luciana", last_name="Díaz",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna78 = User.objects.create_user(username="alumna78", first_name="Lucia", last_name="Cáceres",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna79 = User.objects.create_user(username="alumna79", first_name="Laura", last_name="Mierzo",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna80 = User.objects.create_user(username="alumna80", first_name="Scarlett", last_name="Suarez",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna81 = User.objects.create_user(username="alumna81", first_name="Catalina", last_name="Bravo",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna82 = User.objects.create_user(username="alumna82", first_name="Alejandra", last_name="Muñoz",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna83 = User.objects.create_user(username="alumna83", first_name="Josefa", last_name="Perez",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna84 = User.objects.create_user(username="alumna84", first_name="Josefina", last_name="Quiróz",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna85 = User.objects.create_user(username="alumna85", first_name="Monserrat", last_name="Martinez",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna86 = User.objects.create_user(username="alumna86", first_name="Valentina", last_name="Ruiz",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna87 = User.objects.create_user(username="alumna87", first_name="Margarita", last_name="Elfernan",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna88 = User.objects.create_user(username="alumna88", first_name="Javiera", last_name="Ramos",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna89 = User.objects.create_user(username="alumna89", first_name="María José", last_name="Del Campo",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna90 = User.objects.create_user(username="alumna90", first_name="Kiara", last_name="De la Maza",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna91 = User.objects.create_user(username="alumna91", first_name="Karen", last_name="James",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna92 = User.objects.create_user(username="alumna92", first_name="Sofía", last_name="Toledo",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna93 = User.objects.create_user(username="alumna93", first_name="Agustina", last_name="Timana",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna94 = User.objects.create_user(username="alumna94", first_name="Dominga", last_name="Espinoza",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna95 = User.objects.create_user(username="alumna95", first_name="Asunción", last_name="Gómez",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna96 = User.objects.create_user(username="alumna96", first_name="Karen", last_name="James",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna97 = User.objects.create_user(username="alumna97", first_name="Sofía", last_name="Toledo",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna98 = User.objects.create_user(username="alumna98", first_name="Agustina", last_name="Timana",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna99 = User.objects.create_user(username="alumna99", first_name="Dominga", last_name="Espinoza",
                                                password="contraseña123", es_alumna=True)

    usuaria_alumna100 = User.objects.create_user(username="alumna100", first_name="Asunción", last_name="Gómez",
                                                 password="contraseña123", es_alumna=True)

    ## 30 alumnas
    alumnas1 = [usuaria_alumna1, usuaria_alumna2, usuaria_alumna3, usuaria_alumna4, usuaria_alumna5,
                usuaria_alumna6, usuaria_alumna7, usuaria_alumna8, usuaria_alumna9, usuaria_alumna10,
                usuaria_alumna11, usuaria_alumna12, usuaria_alumna13, usuaria_alumna14, usuaria_alumna15,
                usuaria_alumna16, usuaria_alumna17, usuaria_alumna18, usuaria_alumna19, usuaria_alumna20,
                usuaria_alumna21, usuaria_alumna22, usuaria_alumna23, usuaria_alumna24, usuaria_alumna25,
                usuaria_alumna26, usuaria_alumna27, usuaria_alumna28, usuaria_alumna29, usuaria_alumna30]

    ## 30 alumnas
    alumnas2 = [usuaria_alumna31, usuaria_alumna32, usuaria_alumna33, usuaria_alumna34, usuaria_alumna35,
                usuaria_alumna36, usuaria_alumna37, usuaria_alumna38, usuaria_alumna39, usuaria_alumna40,
                usuaria_alumna41, usuaria_alumna42, usuaria_alumna43, usuaria_alumna44, usuaria_alumna45,
                usuaria_alumna46, usuaria_alumna47, usuaria_alumna48, usuaria_alumna49, usuaria_alumna50,
                usuaria_alumna51, usuaria_alumna52, usuaria_alumna53, usuaria_alumna54, usuaria_alumna55,
                usuaria_alumna56, usuaria_alumna57, usuaria_alumna58, usuaria_alumna59, usuaria_alumna60]

    ## 20 alumnas
    alumnas3 = [usuaria_alumna61, usuaria_alumna62, usuaria_alumna63, usuaria_alumna64, usuaria_alumna65,
                usuaria_alumna66, usuaria_alumna67, usuaria_alumna68, usuaria_alumna69, usuaria_alumna70,
                usuaria_alumna71, usuaria_alumna72, usuaria_alumna73, usuaria_alumna74, usuaria_alumna75,
                usuaria_alumna76, usuaria_alumna77, usuaria_alumna78, usuaria_alumna79, usuaria_alumna80]

    ## 5 alumnas
    alumnas4 = [usuaria_alumna81, usuaria_alumna82, usuaria_alumna83, usuaria_alumna84, usuaria_alumna85]

    ## 5 alumnas
    alumnas5 = [usuaria_alumna86, usuaria_alumna87, usuaria_alumna88, usuaria_alumna89, usuaria_alumna90]

    ## 5 alumnas
    alumnas6 = [usuaria_alumna91, usuaria_alumna92, usuaria_alumna93, usuaria_alumna94, usuaria_alumna95]

    """
    CASOS:
    1. CURSO NORMAL
    2. CURSO SIN ALUMNAS
    3. CURSO SIN CLASES
    4. CURSO SIN ASISTENCIAS
    5. CURSO SIN ALUMNAS NI CLASES
    6. CURSO CON ASISTENCIAS, SIN PROX CLASE CREADA

    C++ básico FCFM - caso 1
    C++ medio FCFM - caso 2
    C++ avanzado FCFM - caso 5

    Python UAndes - caso 2
    Python Antofa - caso 3

    C++ básico UMayor - caso 1
    C++ medio UMayor - caso 4
    C++ avanzado UMayor - caso 6
    """

    ## ALUMNAS INSCRITAS

    def agregaAlumnas(alumnas, curso):
        for alumna in alumnas:
            curso.alumnas.add(alumna)

    agregaAlumnas(alumnas1, curso_basico)
    agregaAlumnas(alumnas2, curso_basico_umayor)
    agregaAlumnas(alumnas5, curso_medio_umayor)

    ## CLASES

    # guardado en la bdd
    clase_basico1 = Clase.objects.create(nombre="Ciclos for", curso=curso_basico, fecha_clase=datetime.date(2020, 4, 4))
    clase_basico2 = Clase.objects.create(nombre="Ciclos while", curso=curso_basico,
                                         fecha_clase=datetime.date(2020, 4, 11))
    clase_basico3 = Clase.objects.create(nombre="Grafos", curso=curso_basico, fecha_clase=datetime.date(2020, 4, 18))
    clase_basico4 = Clase.objects.create(nombre="DBS", curso=curso_basico, fecha_clase=datetime.date(2020, 4, 25))
    clase_basico5 = Clase.objects.create(nombre="DFS", curso=curso_basico, fecha_clase=datetime.date(2020, 5, 2))

    # nuevo
    clase_medio1 = Clase.objects.create(nombre="Arreglos", curso=curso_medio, fecha_clase=datetime.date(2020, 4, 4))
    clase_medio2 = Clase.objects.create(nombre="Variables", curso=curso_medio, fecha_clase=datetime.date(2020, 4, 11))
    clase_medio3 = Clase.objects.create(nombre="Listas Enlazadas", curso=curso_medio,
                                        fecha_clase=datetime.date(2020, 4, 18))
    clase_medio4 = Clase.objects.create(nombre="Intro a la Programación Competitiva", curso=curso_medio,
                                        fecha_clase=datetime.date(2020, 4, 25))
    clase_medio5 = Clase.objects.create(nombre="Intro a la Programación Competitiva 2", curso=curso_medio,
                                        fecha_clase=datetime.date(2020, 5, 2))

    clase_basico_umayor1 = Clase.objects.create(nombre="Clase 1: Ciclos for", curso=curso_basico_umayor,
                                                fecha_clase=datetime.date(2020, 4, 4))
    clase_basico_umayor2 = Clase.objects.create(nombre="Clase 2: Ciclos while", curso=curso_basico_umayor,
                                                fecha_clase=datetime.date(2020, 4, 11))
    clase_basico_umayor3 = Clase.objects.create(nombre="Clase 3: Grafos", curso=curso_basico_umayor,
                                                fecha_clase=datetime.date(2020, 4, 18))
    clase_basico_umayor4 = Clase.objects.create(nombre="Clase 4: DBS", curso=curso_basico_umayor,
                                                fecha_clase=datetime.date(2020, 4, 25))
    clase_basico_umayor5 = Clase.objects.create(nombre="Clase 5: DFS", curso=curso_basico_umayor,
                                                fecha_clase=datetime.date(2020, 5, 2))

    clase_medio_umayor1 = Clase.objects.create(nombre="Clase 1: Arreglos", curso=curso_medio_umayor,
                                               fecha_clase=datetime.date(2020, 4, 4))
    clase_medio_umayor2 = Clase.objects.create(nombre="Clase 2: Variables", curso=curso_medio_umayor,
                                               fecha_clase=datetime.date(2020, 4, 11))
    clase_medio_umayor3 = Clase.objects.create(nombre="Clase 3: Listas Enlazadas", curso=curso_medio_umayor,
                                               fecha_clase=datetime.date(2020, 4, 18))
    clase_medio_umayor4 = Clase.objects.create(nombre="Clase 4: Intro a la Programación Competitiva",
                                               curso=curso_medio_umayor, fecha_clase=datetime.date(2020, 4, 25))
    clase_medio_umayor5 = Clase.objects.create(nombre="Clase 5: Intro a la Programación Competitiva 2",
                                               curso=curso_medio_umayor, fecha_clase=datetime.date(2020, 5, 2))

    ## ASISTENCIAS

    alumnas_basico = alumnas1

    clases_basico = [clase_basico1, clase_basico2, clase_basico3, clase_basico4, clase_basico5,
                     ]

    alumnas_basico_umayor = alumnas2

    clases_basico_umayor = [clase_basico_umayor1, clase_basico_umayor2, clase_basico_umayor3, clase_basico_umayor4,
                            clase_basico_umayor5,
                            ]

    alumnas_avanzado_umayor = alumnas3

    def nuevaAsistencia(clases, alumnas, profesora):
        for clase in clases:
            for alumna in alumnas:
                Asistencia.objects.create(alumna=alumna, clase=clase, asistio=random.randint(0, 1))

    nuevaAsistencia(clases_basico, alumnas_basico, usuaria_profesora)
    nuevaAsistencia(clases_basico_umayor, alumnas_basico_umayor, usuaria_profesora6)
