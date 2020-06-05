from asistencia.models import Asistencia
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




## Calcula el procentaje de asistencia de la alumna con respecto a las clases totales
def porcentaje_asistencia(usuaria, curso):
    nro_clases = max(len(Clase.objects.filter(curso=curso)),curso.cant_clases)
    nro_asistidas = len(Asistencia.objects.filter(clase__curso=curso, alumna=usuaria, asistio=True))

    return int((nro_asistidas/nro_clases)*100)



## Devuelve una lista de bools que indican si la alumna asistio o no a las clases de un curso
def clases_asistencias_alumna(usuaria, curso):
    asistencias = Asistencia.objects.filter(alumna=usuaria, clase__curso=curso).order_by('clase_id')
    lista = []
    for asistencia in asistencias:
        lista += [[asistencia.clase, asistencia.asistio]]
    return lista

