from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.views import View

from asistencia.utils import clases_asistencias_alumna, porcentaje_asistencia, Clase
from cursos.models import Curso
from usuarios.models import User


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

            return render(request, 'cursos/inicio_curso.html', {
                'curso': curso,
                'usuaria': usuaria,
                'porcentaje_asistencia': porcentaje_asistencia(usuaria=usuaria, curso=curso),
                'clases_asistencias': clases_asistencias,
                'nro_clases_totales': max(len(clases_totales), curso.cant_clases),
                'nro_clases_realizadas': len(clases_asistencias)

        })
        else:
            return HttpResponseForbidden("No tienes permiso para acceder a este curso.")


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
