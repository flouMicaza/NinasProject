import random

from usuarios.models import *
from cursos.models import Curso
from asistencia.models import Asistencia
from clases.models import Clase


## CURSOS

# guardado en la bdd
curso_basico = Curso.objects.create(nombre="C++: Básico, FCFM")
curso_medio = Curso.objects.create(nombre="C++: Medio, FCFM")
curso_avanzado = Curso.objects.create(nombre="C++: Avanzado, FCFM")
curso_uandes = Curso.objects.create(nombre="Python Uandes")
curso_antofa = Curso.objects.create(nombre="Python Antofagasta")

# nuevo
curso_basico_umayor = Curso.objects.create(nombre="C++: Básico, UMayor")
curso_medio_umayor = Curso.objects.create(nombre="C++: Medio, UMayor")
curso_avanzado_umayor = Curso.objects.create(nombre="C++: Avanzado, UMayor")



## PROFESORAS

# guardado en la bdd
usuaria_profesora = User.objects.create_user(username="profesora", password="contraseña123",es_profesora=True)
usuaria_profesora2 = User.objects.create_user(username="profesora2", password="contraseña123",es_profesora=True)

# nuevo
usuaria_profesora3= User.objects.create_user(username="profesora3", password="contraseña123",es_profesora=True)
usuaria_profesora4= User.objects.create_user(username="profesora4", password="contraseña123",es_profesora=True)
usuaria_profesora5= User.objects.create_user(username="profesora5", password="contraseña123",es_profesora=True)
usuaria_profesora6= User.objects.create_user(username="profesora6", password="contraseña123",es_profesora=True)
usuaria_profesora7= User.objects.create_user(username="profesora7", password="contraseña123",es_profesora=True)
usuaria_profesora8= User.objects.create_user(username="profesora8", password="contraseña123",es_profesora=True)


## VOLUNTARIAS

# guardado en la bdd
usuaria_voluntaria = User.objects.create_user(username="voluntaria", password="contraseña123",es_voluntaria=True)
usuaria_voluntaria2 = User.objects.create_user(username="voluntaria2", password="contraseña123",es_voluntaria=True)
usuaria_voluntaria3 = User.objects.create_user(username="voluntaria3", password="contraseña123",es_voluntaria=True)
# nuevo
usuaria_voluntaria4 = User.objects.create_user(username="voluntaria4", password="contraseña123",es_voluntaria=True)
usuaria_voluntaria5 = User.objects.create_user(username="voluntaria5", password="contraseña123",es_voluntaria=True)
usuaria_voluntaria6 = User.objects.create_user(username="voluntaria6", password="contraseña123",es_voluntaria=True)
usuaria_voluntaria7 = User.objects.create_user(username="voluntaria7", password="contraseña123",es_voluntaria=True)
usuaria_voluntaria8 = User.objects.create_user(username="voluntaria8", password="contraseña123",es_voluntaria=True)
usuaria_voluntaria9 = User.objects.create_user(username="voluntaria9", password="contraseña123",es_voluntaria=True)


## RELACIONES USUARIAS CURSOS

# ya esta en la bdd
curso_basico.profesoras.add(usuaria_profesora)
curso_medio.profesoras.add(usuaria_profesora2)
curso_avanzado.profesoras.add(usuaria_profesora3)
curso_uandes.profesoras.add(usuaria_profesora4)
curso_antofa.profesoras.add(usuaria_profesora5)

# nuevo
curso_basico_umayor.profesoras.add(usuaria_profesora6)
curso_medio_umayor.profesoras.add(usuaria_profesora7)
curso_avanzado_umayor.profesoras.add(usuaria_profesora8)



# ya esta en la bdd
curso_basico.voluntarias.add(usuaria_voluntaria)
curso_basico.voluntarias.add(usuaria_voluntaria2)

curso_medio.voluntarias.add(usuaria_voluntaria2)
curso_medio.voluntarias.add(usuaria_voluntaria3)

curso_avanzado.voluntarias.add(usuaria_voluntaria3)
curso_avanzado.voluntarias.add(usuaria_voluntaria4)

curso_uandes.voluntarias.add(usuaria_voluntaria4)
curso_uandes.voluntarias.add(usuaria_voluntaria5)

curso_antofa.voluntarias.add(usuaria_voluntaria5)
curso_antofa.voluntarias.add(usuaria_voluntaria6)

# nuevo
curso_basico_umayor.voluntarias.add(usuaria_voluntaria6)
curso_basico_umayor.voluntarias.add(usuaria_voluntaria7)

curso_medio_umayor.voluntarias.add(usuaria_voluntaria7)
curso_medio_umayor.voluntarias.add(usuaria_voluntaria8)

curso_avanzado_umayor.voluntarias.add(usuaria_voluntaria8)
curso_avanzado_umayor.voluntarias.add(usuaria_voluntaria9)



## ya esta en la bdd
usuaria_alumna1 = User.objects.create_user(username="alumna1", first_name="Juana", last_name="Perez", password="contraseña123", es_alumna=True)

usuaria_alumna2 = User.objects.create_user(username="alumna2", first_name="Claudia", last_name="Muñoz", password="contraseña123", es_alumna=True)

usuaria_alumna3 = User.objects.create_user(username="alumna3", first_name="Claudia", last_name="Briones", password="contraseña123", es_alumna=True)

usuaria_alumna4 = User.objects.create_user(username="alumna4", first_name="Claudia", last_name="Opazo", password="contraseña123", es_alumna=True)

usuaria_alumna5 = User.objects.create_user(username="alumna5", first_name="Antonia", last_name="Quezada", password="contraseña123", es_alumna=True)

## por agregar a la bdd
usuaria_alumna6 = User.objects.create_user(username="alumna6", first_name="Fernanda", last_name="Macías", password="contraseña123", es_alumna=True)

usuaria_alumna7 = User.objects.create_user(username="alumna7", first_name="Ignacia", last_name="Macías", password="contraseña123", es_alumna=True)

usuaria_alumna8 = User.objects.create_user(username="alumna8", first_name="Ignacia", last_name="Labarca", password="contraseña123", es_alumna=True)

usuaria_alumna9 = User.objects.create_user(username="alumna9", first_name="Karina", last_name="Rozas", password="contraseña123", es_alumna=True)

usuaria_alumna10 = User.objects.create_user(username="alumna10", first_name="Florencia", last_name="Manríquez", password="contraseña123", es_alumna=True)

usuaria_alumna11 = User.objects.create_user(username="alumna11", first_name="Antonia", last_name="Jimenez", password="contraseña123", es_alumna=True)

usuaria_alumna12 = User.objects.create_user(username="alumna12", first_name="Constanza", last_name="Mora", password="contraseña123", es_alumna=True)

usuaria_alumna13 = User.objects.create_user(username="alumna13", first_name="Rosario", last_name="González", password="contraseña123", es_alumna=True)

usuaria_alumna14 = User.objects.create_user(username="alumna14", first_name="Lupe", last_name="Rojas", password="contraseña123", es_alumna=True)

usuaria_alumna15 = User.objects.create_user(username="alumna15", first_name="Martina", last_name="Monsalves", password="contraseña123", es_alumna=True)

usuaria_alumna16 = User.objects.create_user(username="alumna16", first_name="Belén", last_name="Acevedo", password="contraseña123", es_alumna=True)

usuaria_alumna17 = User.objects.create_user(username="alumna17", first_name="Francisca", last_name="Riquelme", password="contraseña123", es_alumna=True)

usuaria_alumna18 = User.objects.create_user(username="alumna18", first_name="Gabriela", last_name="Herrera", password="contraseña123", es_alumna=True)

usuaria_alumna19 = User.objects.create_user(username="alumna19", first_name="Francisca", last_name="Fabres", password="contraseña123", es_alumna=True)

usuaria_alumna20 = User.objects.create_user(username="alumna20", first_name="Bárbara", last_name="Fuentes", password="contraseña123", es_alumna=True)

usuaria_alumna21 = User.objects.create_user(username="alumna21", first_name="Paula", last_name="Cifuentes", password="contraseña123", es_alumna=True)

usuaria_alumna22 = User.objects.create_user(username="alumna22", first_name="Paulina", last_name="Lagos", password="contraseña123", es_alumna=True)

usuaria_alumna23 = User.objects.create_user(username="alumna23", first_name="Alejandra", last_name="Rivas", password="contraseña123", es_alumna=True)

usuaria_alumna24 = User.objects.create_user(username="alumna24", first_name="Mabel", last_name="Recabarren", password="contraseña123", es_alumna=True)

usuaria_alumna25 = User.objects.create_user(username="alumna25", first_name="Teresa", last_name="Paredes", password="contraseña123", es_alumna=True)

usuaria_alumna26 = User.objects.create_user(username="alumna26", first_name="Alicia", last_name="Cuadra", password="contraseña123", es_alumna=True)

usuaria_alumna27 = User.objects.create_user(username="alumna27", first_name="Cecilia", last_name="Poblete", password="contraseña123", es_alumna=True)

usuaria_alumna28 = User.objects.create_user(username="alumna28", first_name="Marta", last_name="Osorio", password="contraseña123", es_alumna=True)

usuaria_alumna29 = User.objects.create_user(username="alumna29", first_name="Natalia", last_name="Arce", password="contraseña123", es_alumna=True)

usuaria_alumna30 = User.objects.create_user(username="alumna30", first_name="Daniela", last_name="Medina", password="contraseña123", es_alumna=True)

usuaria_alumna31 = User.objects.create_user(username="alumna31", first_name="Gabriela", last_name="Cuadra", password="contraseña123", es_alumna=True)

usuaria_alumna32 = User.objects.create_user(username="alumna32", first_name="Luciana", last_name="Díaz", password="contraseña123", es_alumna=True)

usuaria_alumna33 = User.objects.create_user(username="alumna33", first_name="Lucia", last_name="Cáceres", password="contraseña123", es_alumna=True)

usuaria_alumna34 = User.objects.create_user(username="alumna34", first_name="Laura", last_name="Mierzo", password="contraseña123", es_alumna=True)

usuaria_alumna35 = User.objects.create_user(username="alumna35", first_name="Scarlett", last_name="Suarez", password="contraseña123", es_alumna=True)

usuaria_alumna36 = User.objects.create_user(username="alumna36", first_name="Catalina", last_name="Bravo", password="contraseña123", es_alumna=True)

usuaria_alumna37 = User.objects.create_user(username="alumna37", first_name="Alejandra", last_name="Muñoz", password="contraseña123", es_alumna=True)

usuaria_alumna38 = User.objects.create_user(username="alumna38", first_name="Josefa", last_name="Perez", password="contraseña123", es_alumna=True)

usuaria_alumna39 = User.objects.create_user(username="alumna39", first_name="Josefina", last_name="Quiróz", password="contraseña123", es_alumna=True)

usuaria_alumna40 = User.objects.create_user(username="alumna40", first_name="Monserrat", last_name="Martinez", password="contraseña123", es_alumna=True)

usuaria_alumna41 = User.objects.create_user(username="alumna41", first_name="Valentina", last_name="Ruiz", password="contraseña123", es_alumna=True)

usuaria_alumna42 = User.objects.create_user(username="alumna42", first_name="Margarita", last_name="Elfernan", password="contraseña123", es_alumna=True)

usuaria_alumna43 = User.objects.create_user(username="alumna43", first_name="Javiera", last_name="Ramos", password="contraseña123", es_alumna=True)

usuaria_alumna44 = User.objects.create_user(username="alumna44", first_name="María José", last_name="Del Campo", password="contraseña123", es_alumna=True)

usuaria_alumna45 = User.objects.create_user(username="alumna45", first_name="Kiara", last_name="De la Maza", password="contraseña123", es_alumna=True)

usuaria_alumna46 = User.objects.create_user(username="alumna46", first_name="Karen", last_name="James", password="contraseña123", es_alumna=True)

usuaria_alumna47 = User.objects.create_user(username="alumna47", first_name="Sofía", last_name="Toledo", password="contraseña123", es_alumna=True)

usuaria_alumna48 = User.objects.create_user(username="alumna48", first_name="Agustina", last_name="Timana", password="contraseña123", es_alumna=True)

usuaria_alumna49 = User.objects.create_user(username="alumna49", first_name="Dominga", last_name="Espinoza", password="contraseña123", es_alumna=True)

usuaria_alumna50 = User.objects.create_user(username="alumna50", first_name="Asunción", last_name="Gómez", password="contraseña123", es_alumna=True)


"""
CASOS:
1. CURSO NORMAL
2. CURSO SIN ALUMNAS
3. CURSO SIN CLASES
4. CURSO SIN ASISTENCIAS
5. SIN ALUMNAS NI CLASES

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
curso_basico.alumnas.add(usuaria_alumna1)
curso_basico.alumnas.add(usuaria_alumna2)
curso_basico.alumnas.add(usuaria_alumna3)
curso_basico.alumnas.add(usuaria_alumna4)
curso_basico.alumnas.add(usuaria_alumna5)
curso_basico.alumnas.add(usuaria_alumna6)
curso_basico.alumnas.add(usuaria_alumna7)
curso_basico.alumnas.add(usuaria_alumna8)
curso_basico.alumnas.add(usuaria_alumna9)
curso_basico.alumnas.add(usuaria_alumna10)
curso_basico.alumnas.add(usuaria_alumna11)
curso_basico.alumnas.add(usuaria_alumna12)
curso_basico.alumnas.add(usuaria_alumna13)
curso_basico.alumnas.add(usuaria_alumna14)
curso_basico.alumnas.add(usuaria_alumna15)
curso_basico.alumnas.add(usuaria_alumna16)
curso_basico.alumnas.add(usuaria_alumna17)
curso_basico.alumnas.add(usuaria_alumna18)
curso_basico.alumnas.add(usuaria_alumna19)
curso_basico.alumnas.add(usuaria_alumna20)
curso_basico.alumnas.add(usuaria_alumna21)
curso_basico.alumnas.add(usuaria_alumna22)
curso_basico.alumnas.add(usuaria_alumna23)
curso_basico.alumnas.add(usuaria_alumna24)
curso_basico.alumnas.add(usuaria_alumna25)


curso_antofa.alumnas.add(usuaria_alumna26)
curso_antofa.alumnas.add(usuaria_alumna27)
curso_antofa.alumnas.add(usuaria_alumna28)
curso_antofa.alumnas.add(usuaria_alumna29)
curso_antofa.alumnas.add(usuaria_alumna30)


curso_basico_umayor.alumnas.add(usuaria_alumna31)
curso_basico_umayor.alumnas.add(usuaria_alumna32)
curso_basico_umayor.alumnas.add(usuaria_alumna33)
curso_basico_umayor.alumnas.add(usuaria_alumna34)
curso_basico_umayor.alumnas.add(usuaria_alumna35)
curso_basico_umayor.alumnas.add(usuaria_alumna36)
curso_basico_umayor.alumnas.add(usuaria_alumna37)
curso_basico_umayor.alumnas.add(usuaria_alumna38)
curso_basico_umayor.alumnas.add(usuaria_alumna39)
curso_basico_umayor.alumnas.add(usuaria_alumna40)
curso_basico_umayor.alumnas.add(usuaria_alumna41)
curso_basico_umayor.alumnas.add(usuaria_alumna42)
curso_basico_umayor.alumnas.add(usuaria_alumna43)
curso_basico_umayor.alumnas.add(usuaria_alumna44)
curso_basico_umayor.alumnas.add(usuaria_alumna45)
curso_basico_umayor.alumnas.add(usuaria_alumna46)
curso_basico_umayor.alumnas.add(usuaria_alumna47)
curso_basico_umayor.alumnas.add(usuaria_alumna48)
curso_basico_umayor.alumnas.add(usuaria_alumna49)
curso_basico_umayor.alumnas.add(usuaria_alumna50)


curso_medio_umayor.alumnas.add(usuaria_alumna1)
curso_medio_umayor.alumnas.add(usuaria_alumna2)
curso_medio_umayor.alumnas.add(usuaria_alumna3)
curso_medio_umayor.alumnas.add(usuaria_alumna4)
curso_medio_umayor.alumnas.add(usuaria_alumna5)


curso_avanzado_umayor.alumnas.add(usuaria_alumna6)
curso_avanzado_umayor.alumnas.add(usuaria_alumna7)
curso_avanzado_umayor.alumnas.add(usuaria_alumna8)
curso_avanzado_umayor.alumnas.add(usuaria_alumna9)
curso_avanzado_umayor.alumnas.add(usuaria_alumna10)
curso_avanzado_umayor.alumnas.add(usuaria_alumna11)
curso_avanzado_umayor.alumnas.add(usuaria_alumna12)
curso_avanzado_umayor.alumnas.add(usuaria_alumna13)
curso_avanzado_umayor.alumnas.add(usuaria_alumna14)
curso_avanzado_umayor.alumnas.add(usuaria_alumna15)
curso_avanzado_umayor.alumnas.add(usuaria_alumna16)
curso_avanzado_umayor.alumnas.add(usuaria_alumna17)
curso_avanzado_umayor.alumnas.add(usuaria_alumna18)
curso_avanzado_umayor.alumnas.add(usuaria_alumna19)
curso_avanzado_umayor.alumnas.add(usuaria_alumna20)
curso_avanzado_umayor.alumnas.add(usuaria_alumna21)
curso_avanzado_umayor.alumnas.add(usuaria_alumna22)
curso_avanzado_umayor.alumnas.add(usuaria_alumna23)
curso_avanzado_umayor.alumnas.add(usuaria_alumna24)
curso_avanzado_umayor.alumnas.add(usuaria_alumna25)



## CLASES

# guardado en la bdd
clase_basico1 = Clase.objects.create(nombre="Clase 1: Ciclos for", curso=curso_basico)
clase_basico2 = Clase.objects.create(nombre="Clase 2: Ciclos while", curso=curso_basico)
clase_basico3 = Clase.objects.create(nombre="Clase 3: Grafos", curso=curso_basico)
clase_basico4 = Clase.objects.create(nombre="Clase 4: DBS", curso=curso_basico)
clase_basico5 = Clase.objects.create(nombre="Clase 5: DFS", curso=curso_basico)
clase_basico6 = Clase.objects.create(nombre="Clase 6: Dijkstra", curso=curso_basico)
clase_basico7 = Clase.objects.create(nombre="Clase 7: Coloración de Grafos", curso=curso_basico)
clase_basico8 = Clase.objects.create(nombre="Clase 8: Arboles", curso=curso_basico)
clase_basico9 = Clase.objects.create(nombre="Clase 9: Árbol Cobertor", curso=curso_basico)
clase_basico10 = Clase.objects.create(nombre="Clase 10: Programación Oridentada a Objectos", curso=curso_basico)
clase_basico11 = Clase.objects.create(nombre="Clase 11: Super Clases", curso=curso_basico)
clase_basico12 = Clase.objects.create(nombre="Clase 12: Interfaz", curso=curso_basico)
clase_basico13 = Clase.objects.create(nombre="Clase 13: Computadores", curso=curso_basico)
clase_basico14 = Clase.objects.create(nombre="Clase 14: Historia de la Computación", curso=curso_basico)

# nuevo
clase_medio1 = Clase.objects.create(nombre="Clase 1: Arreglos", curso=curso_medio)
clase_medio2 = Clase.objects.create(nombre="Clase 2: Variables", curso=curso_medio)
clase_medio3 = Clase.objects.create(nombre="Clase 3: Listas Enlazadas", curso=curso_medio)
clase_medio4 = Clase.objects.create(nombre="Clase 4: Intro a la Programación Competitiva", curso=curso_medio)
clase_medio5 = Clase.objects.create(nombre="Clase 5: Intro a la Programación Competitiva 2", curso=curso_medio)
clase_medio6 = Clase.objects.create(nombre="Clase 6: Intro a los Grafos", curso=curso_medio)
clase_medio7 = Clase.objects.create(nombre="Clase 7: Intro a los Arboles", curso=curso_medio)
clase_medio8 = Clase.objects.create(nombre="Clase 8: Intro a los Arboles 2 ", curso=curso_medio)
clase_medio9 = Clase.objects.create(nombre="Clase 9: Programación Dinámica ", curso=curso_medio)
clase_medio10 = Clase.objects.create(nombre="Clase 10: Programación Dinámica 2 ", curso=curso_medio)
clase_medio11 = Clase.objects.create(nombre="Clase 11: Super Clases ", curso=curso_medio)


clase_uandes1 = Clase.objects.create(nombre="Clase 1: Variables", curso=curso_uandes)
clase_uandes2 = Clase.objects.create(nombre="Clase 2: Funciones", curso=curso_uandes)
clase_uandes3 = Clase.objects.create(nombre="Clase 3: Ciclos for", curso=curso_uandes)
clase_uandes4 = Clase.objects.create(nombre="Clase 4: Ciclos while", curso=curso_uandes)
clase_uandes5 = Clase.objects.create(nombre="Clase 5: Clases", curso=curso_uandes)
clase_uandes6 = Clase.objects.create(nombre="Clase 6: Objetos", curso=curso_uandes)


clase_basico_umayor1 = Clase.objects.create(nombre="Clase 1: Ciclos for", curso=curso_basico_umayor)
clase_basico_umayor2 = Clase.objects.create(nombre="Clase 2: Ciclos while", curso=curso_basico_umayor)
clase_basico_umayor3 = Clase.objects.create(nombre="Clase 3: Grafos", curso=curso_basico_umayor)
clase_basico_umayor4 = Clase.objects.create(nombre="Clase 4: DBS", curso=curso_basico_umayor)
clase_basico_umayor5 = Clase.objects.create(nombre="Clase 5: DFS", curso=curso_basico_umayor)
clase_basico_umayor6 = Clase.objects.create(nombre="Clase 6: Dijkstra", curso=curso_basico_umayor)
clase_basico_umayor7 = Clase.objects.create(nombre="Clase 7: Coloración de Grafos", curso=curso_basico_umayor)
clase_basico_umayor8 = Clase.objects.create(nombre="Clase 8: Arboles", curso=curso_basico_umayor)
clase_basico_umayor9 = Clase.objects.create(nombre="Clase 9: Árbol Cobertor", curso=curso_basico_umayor)
clase_basico_umayor10 = Clase.objects.create(nombre="Clase 10: Programación Oridentada a Objectos", curso=curso_basico_umayor)
clase_basico_umayor11 = Clase.objects.create(nombre="Clase 11: Super Clases", curso=curso_basico_umayor)
clase_basico_umayor12 = Clase.objects.create(nombre="Clase 12: Interfaz", curso=curso_basico_umayor)
clase_basico_umayor13 = Clase.objects.create(nombre="Clase 13: Computadores", curso=curso_basico_umayor)


clase_medio_umayor1 = Clase.objects.create(nombre="Clase 1: Arreglos", curso=curso_medio_umayor)
clase_medio_umayor2 = Clase.objects.create(nombre="Clase 2: Variables", curso=curso_medio_umayor)
clase_medio_umayor3 = Clase.objects.create(nombre="Clase 3: Listas Enlazadas", curso=curso_medio_umayor)
clase_medio_umayor4 = Clase.objects.create(nombre="Clase 4: Intro a la Programación Competitiva", curso=curso_medio_umayor)
clase_medio_umayor5 = Clase.objects.create(nombre="Clase 5: Intro a la Programación Competitiva 2", curso=curso_medio_umayor)
clase_medio_umayor6 = Clase.objects.create(nombre="Clase 6: Intro a los Grafos", curso=curso_medio_umayor)
clase_medio_umayor7 = Clase.objects.create(nombre="Clase 7: Intro a los Arboles", curso=curso_medio_umayor)
clase_medio_umayor8 = Clase.objects.create(nombre="Clase 8: Intro a los Arboles 2 ", curso=curso_medio_umayor)
clase_medio_umayor9 = Clase.objects.create(nombre="Clase 9: Programación Dinámica ", curso=curso_medio_umayor)
clase_medio_umayor10 = Clase.objects.create(nombre="Clase 10: Programación Dinámica 2 ", curso=curso_medio_umayor)
clase_medio_umayor11 = Clase.objects.create(nombre="Clase 11: Super Clases ", curso=curso_medio_umayor)


clase_avanzado_umayor1 = Clase.objects.create(nombre="Clase 1: Intro a la Programacion Competitiva", curso=curso_medio_umayor)
clase_avanzado_umayor2 = Clase.objects.create(nombre="Clase 2: Intro a la Programacion Competitiva 2", curso=curso_medio_umayor)
clase_avanzado_umayor3 = Clase.objects.create(nombre="Clase 3: Problemas OCI 2012", curso=curso_medio_umayor)
clase_avanzado_umayor4 = Clase.objects.create(nombre="Clase 4: Problemas OCI 2013", curso=curso_medio_umayor)
clase_avanzado_umayor5 = Clase.objects.create(nombre="Clase 5: Problemas OCI 2014", curso=curso_medio_umayor)
clase_avanzado_umayor6 = Clase.objects.create(nombre="Clase 6: Problemas OCI 2015", curso=curso_medio_umayor)
clase_avanzado_umayor7 = Clase.objects.create(nombre="Clase 7: Problemas OCI 2016", curso=curso_medio_umayor)
clase_avanzado_umayor8 = Clase.objects.create(nombre="Clase 8: Problemas OCI 2017", curso=curso_medio_umayor)
clase_avanzado_umayor9 = Clase.objects.create(nombre="Clase 9: Problemas OCI 2018", curso=curso_medio_umayor)
clase_avanzado_umayor10 = Clase.objects.create(nombre="Clase 10: Problemas OCI 2019", curso=curso_medio_umayor)



## ASISTENCIAS

alumnas_basico = [usuaria_alumna1, usuaria_alumna2, usuaria_alumna3, usuaria_alumna4, usuaria_alumna5,
                  usuaria_alumna6, usuaria_alumna7, usuaria_alumna8, usuaria_alumna9, usuaria_alumna10,
                  usuaria_alumna11, usuaria_alumna12, usuaria_alumna13, usuaria_alumna14, usuaria_alumna15,
                  usuaria_alumna16, usuaria_alumna17, usuaria_alumna18, usuaria_alumna19, usuaria_alumna20,
                  usuaria_alumna21, usuaria_alumna22, usuaria_alumna23, usuaria_alumna24, usuaria_alumna25]

clases_basico = [clase_basico1, clase_basico2, clase_basico3, clase_basico4, clase_basico5,
                  clase_basico6, clase_basico7, clase_basico8, clase_basico9, clase_basico10,
                  clase_basico11, clase_basico12, clase_basico13]

alumnas_basico_umayor = [usuaria_alumna31, usuaria_alumna32, usuaria_alumna33, usuaria_alumna34, usuaria_alumna35,
                  usuaria_alumna36, usuaria_alumna37, usuaria_alumna38, usuaria_alumna39, usuaria_alumna40,
                  usuaria_alumna41, usuaria_alumna42, usuaria_alumna43, usuaria_alumna44, usuaria_alumna45,
                  usuaria_alumna46, usuaria_alumna47, usuaria_alumna48, usuaria_alumna49, usuaria_alumna50]

clases_basico_umayor = [clase_basico_umayor1, clase_basico_umayor2, clase_basico_umayor3, clase_basico_umayor4, clase_basico_umayor5,
                        clase_basico_umayor6, clase_basico_umayor7, clase_basico_umayor8, clase_basico_umayor9, clase_basico_umayor10,
                        clase_basico_umayor11, clase_basico_umayor12, clase_basico_umayor13]

alumnas_avanzado_umayor = [usuaria_alumna6, usuaria_alumna7, usuaria_alumna8, usuaria_alumna9, usuaria_alumna10,
                           usuaria_alumna11, usuaria_alumna12, usuaria_alumna13, usuaria_alumna14, usuaria_alumna15,
                           usuaria_alumna16, usuaria_alumna17, usuaria_alumna18, usuaria_alumna19, usuaria_alumna20,
                           usuaria_alumna21, usuaria_alumna22, usuaria_alumna23, usuaria_alumna24, usuaria_alumna25]

clases_avanzado_umayor = [clase_avanzado_umayor1, clase_avanzado_umayor2, clase_avanzado_umayor3, clase_avanzado_umayor4, clase_avanzado_umayor5,
                          clase_avanzado_umayor6, clase_avanzado_umayor7, clase_avanzado_umayor8, clase_avanzado_umayor9, clase_avanzado_umayor10]



def nuevaAsistencia(clases, alumnas, profesora):
    for clase in clases:
        for alumna in alumnas:
            Asistencia.objects.create(alumna=alumna, clase=clase, author=profesora, asistio=random.randint(0, 1))




nuevaAsistencia(clases_basico, alumnas_basico, usuaria_profesora)
nuevaAsistencia(clases_basico_umayor, alumnas_basico_umayor, usuaria_profesora6)
nuevaAsistencia(clases_avanzado_umayor, alumnas_avanzado_umayor, usuaria_profesora8)



