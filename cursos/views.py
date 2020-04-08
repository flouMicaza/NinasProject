from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.views import View
from django.forms import modelform_factory, HiddenInput
from asistencia.utils import clases_asistencias_alumna, porcentaje_asistencia, Clase

from clases.models import Clase
from cursos.models import Curso
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

        if curso in self.get_cursos(request.user.username):
            usuaria = request.user
            clases_totales = Clase.objects.filter(curso=curso)
            clases_asistencias = clases_asistencias_alumna(usuaria=usuaria, curso=curso)

            parameters = {
                'curso': curso,
                'usuaria': usuaria,
                'clases' : clases_totales,
                'porcentaje_asistencia': porcentaje_asistencia(usuaria=usuaria, curso=curso),
                'clases_asistencias': clases_asistencias,
                'nro_clases_totales': max(len(clases_totales), curso.cant_clases),
                'nro_clases_realizadas': len(clases_asistencias)
            }
            return render(request, 'cursos/inicio_curso.html', parameters)
        else:
            return HttpResponseForbidden("No tienes permiso para acceder a este curso.")

    def post(self, request,**kwargs):
        id_clase = request.POST['id_clase']
        clase_edit = Clase.objects.get(id=id_clase)
        if request.POST.get('publica'):
            clase_edit.publica = True
        else:
            clase_edit.publica = False

        if request.POST.get('nombre'):
            clase_edit.nombre = request.POST['nombre']

        if request.POST.get('fecha_clase'):
            #no puede haber dos clases un mismo día.
            clase_mismo_dia = Clase.objects.filter(fecha_clase=request.POST.get('fecha_clase'))
            if len(clase_mismo_dia) == 0 or clase_mismo_dia.first()==clase_edit:
                clase_edit.fecha_clase = request.POST['fecha_clase']
            else:
                messages.success(request,"No se actualizó la fecha, ya existe una clase para ese día")

        clase_edit.save()
        return HttpResponseRedirect(reverse('cursos:curso',kwargs=kwargs))

class MisCursosView(CursosView):

    def get(self, request):
        if request.user.es_profesora  or request.user.es_voluntaria :
            cursos = self.get_cursos(request.user.username)
            return render(request, 'cursos/mis_cursos.html', {'cursos': cursos})
        else:
            return HttpResponseRedirect(reverse('usuarios:index'))


class EstadisticasView(LoginRequiredMixin, View):
    login_url = 'usuarios:login'
    redirect_field_name = ''

    def get(self, request, **kwargs):
        mensaje = "este curso", kwargs["curso_id"]
        return HttpResponse(mensaje)
