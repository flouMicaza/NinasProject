from asistencia.models import Asistencia
from usuarios.models import *
from cursos.models import *
from clases.models import *

## Recibe las alumnas de un curso y las ordena alfabeticamente
def get_alumnas_en_orden(alumnas):
    alum_por_nombre = alumnas.order_by('first_name')
    nro_alumnas = len(alumnas)
    lista_alumnas = []
    i = 0

    while (len(lista_alumnas) < nro_alumnas):
        name = alum_por_nombre[i].first_name
        alum = alumnas.filter(first_name=name).order_by('last_name')

        for alumna in alum:
            lista_alumnas += [alumna]
            i += 1

    return lista_alumnas


## Entrega el curso si la usuaria tiene permiso para acceder a el
def get_cursos(usuaria, curso_id):
    if usuaria.es_profesora:
        cursos = Curso.objects.filter(profesoras__in=[usuaria], id=curso_id)
    elif usuaria.es_voluntaria:
        cursos = Curso.objects.filter(voluntarias__in=[usuaria], id=curso_id)
    elif usuaria.es_alumna:
        cursos = Curso.objects.filter(alumnas__in=[usuaria], id=curso_id)

    if len(cursos) > 0:
        return cursos[0]
    return None


## Entrega la clase si esta corresponde al curso ingresado
def get_clases(curso_id, clase_id):
    clases = Clase.objects.filter(curso_id=curso_id, id=clase_id)
    if len(clases) > 0:
        return clases[0]
    return None


## Calcula el procentaje de asistencia de la alumna con respecto a las clases totales
def porcentaje_asistencia(usuaria, curso):
    nro_clases = len(Clase.objects.filter(curso=curso))
    nro_asistidas = len(Asistencia.objects.filter(clase__curso=curso, alumna=usuaria, asistio=True))

    return (nro_asistidas/nro_clases)*100



## Devuelve una lista de bools que indican si la alumna asistio o no a las clases de un curso
def clases_asistencias_alumna(usuaria, curso):
    asistencias = Asistencia.objects.filter(alumna=usuaria, clase__curso=curso).order_by('clase_id')
    lista = []
    for asistencia in asistencias:
        lista += [[asistencia.clase, asistencia.asistio]]
    return lista









