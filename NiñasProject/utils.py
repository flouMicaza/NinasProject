from clases.models import Clase
from cursos.models import Curso

## Entrega el curso si la usuaria tiene permiso para acceder a el
from problemas.models import Caso

'''
Método que entrega el curso correspondiente a curso_id solo si la usuaria pertenece al curso. 
'''
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


'''
Entrega la clase si esta corresponde al curso ingresado
'''
def get_clases(curso_id, clase_id):
    clases = Clase.objects.filter(curso_id=curso_id, id=clase_id)
    if len(clases) > 0:
        return clases[0]
    return None


'''
Método que entrega tests feedback clasificados por categoría.
'''
def get_ordered_test_feedback(test_feedbacks, problema):
    categorías = Caso.objects.filter(problema=problema).values('categoría').distinct()
    result = []
    for d in categorías:
        dic = {'categoría': d}
        dic['test_feedback'] = test_feedbacks.filter(caso__categoría=d['categoría'])
        dic['casos_buenos'] = dic['test_feedback'].filter(passed=True).count()
        dic['casos_malos'] = dic['test_feedback'].filter(passed=False).count()
        result.append(dic)
    return result
