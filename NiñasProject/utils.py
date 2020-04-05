from clases.models import Clase
from cursos.models import Curso

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