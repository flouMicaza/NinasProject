from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from NiñasProject.decorators import docente_required
from asistencia.utils import clases_asistencias_alumna, porcentaje_asistencia

from clases.models import Clase
from cursos.models import Curso
from feedback.models import Feedback
from usuarios.models import User

#Vista padre de los cursos
class CursosView(LoginRequiredMixin, View):
    login_url = 'usuarios:login'
    redirect_field_name = ''

    def get_cursos(self, username):
        """
        Método que entrega los cursos en los que username es docente
        :param username: usuario a buscar
        :return: lista de cursos
        """
        usuaria = User.objects.get(username=username)
        if usuaria.es_profesora:
            cursos = Curso.objects.filter(profesoras__in=[usuaria])
        elif usuaria.es_voluntaria:
            cursos = Curso.objects.filter(voluntarias__in=[usuaria])
        elif usuaria.es_alumna:
            cursos = Curso.objects.filter(alumnas__in=[usuaria])
        return list(cursos)


class CursoView(CursosView):

    def get(self, request, **kwargs ):
        curso_id = kwargs['curso_id']
        curso = get_object_or_404(Curso, pk=curso_id)
        if 'order' not in kwargs:
            orden = 'oldest'
        else:
            orden = kwargs['order']

        if curso in self.get_cursos(request.user.username):
            usuaria = request.user
            clases_totales = Clase.objects.filter(curso=curso)
            if orden == 'newest':
                clases_totales = clases_totales.order_by('-fecha_clase')
            clases_asistencias = clases_asistencias_alumna(usuaria=usuaria, curso=curso)
            feedbacks = self.get_feedbacks_alumna(usuaria,clases_totales)

            parameters = {
                'curso': curso,
                'usuaria': usuaria,
                'clases' : clases_totales,
                'porcentaje_asistencia': porcentaje_asistencia(usuaria=usuaria, curso=curso),
                'clases_asistencias': clases_asistencias,
                'nro_clases_totales': max(len(clases_totales), curso.cant_clases),
                'nro_clases_realizadas': len(clases_asistencias),
                'feedbacks':feedbacks,
                'order': orden
            }
            return render(request, 'cursos/inicio_curso.html', parameters)
        else:
            messages.success(request, "No tienes permiso para ver ese curso")
            return HttpResponseRedirect(reverse('usuarios:index'))

    def post(self, request,**kwargs):
        id_clase = request.POST['id_clase']
        clase_edit = Clase.objects.get(id=id_clase)
        edit_correct = True

        if request.POST.get('fecha_clase'):
            #no puede haber dos clases un mismo día.
            clase_mismo_dia = Clase.objects.filter(fecha_clase=request.POST.get('fecha_clase'),curso=clase_edit.curso)
            if len(clase_mismo_dia) == 0 or clase_mismo_dia.first()==clase_edit:
                clase_edit.fecha_clase = request.POST['fecha_clase']
            else:
                messages.success(request,f"No se actualizó la clase {clase_edit.nombre}, ya existe una clase para la fecha ingresada")
                edit_correct = False

        if edit_correct:
            if request.POST.get('publica'):
                clase_edit.publica = True
            else:
                clase_edit.publica = False

            if request.POST.get('nombre'):
                clase_edit.nombre = request.POST['nombre']
            messages.success(request, "La clase se editó correctamente")

        clase_edit.save()
        return HttpResponseRedirect(reverse('cursos:curso',kwargs=kwargs))

    def get_feedbacks_alumna(self, usuaria, clases_totales):
        result = {}
        for clase in clases_totales:
            for problema in clase.problema_set.all():
                result[problema.id] = Feedback.objects.filter(user=usuaria, problema=problema).order_by('fecha_envio').last()
        return result

@method_decorator([docente_required], name='dispatch')
class MisCursosView(CursosView):

    def get(self, request):
        if request.user.es_profesora  or request.user.es_voluntaria :
            cursos = self.get_cursos(request.user.username)
            return render(request, 'cursos/mis_cursos.html', {'cursos': cursos})
        else:
            return HttpResponseRedirect(reverse('usuarios:index'))


@method_decorator([docente_required], name='dispatch')
class EstadisticasView(LoginRequiredMixin, View):
    login_url = 'usuarios:login'
    redirect_field_name = ''

    def get(self, request, **kwargs):
        curso_id = kwargs["curso_id"]
        curso = get_object_or_404(Curso, id=curso_id, profesoras__in=[request.user])
        clases = Clase.objects.filter(curso=curso, publica=True)
        feedback_alumnas = self.get_feedbacks_curso(curso)
        return render(request, 'cursos/tabla_estadisticas.html', {'curso': curso,'clases':clases, 'feedback_alumnas':feedback_alumnas})


    def get_feedbacks_curso(self, curso):
        clases = Clase.objects.filter(curso=curso, publica=True)
        alumnas = curso.alumnas.all()
        result = {}
        for alumna in alumnas:
            alu_resultado = {'alumna': alumna, 'feedbacks': {}}
            for clase in clases:
                for problema in clase.problema_set.all():
                    feedback = Feedback.objects.filter(user=alumna, problema=problema).order_by('fecha_envio').last()
                    alu_resultado['feedbacks'][problema.id] = feedback
            result[alumna.id] = alu_resultado
        return result