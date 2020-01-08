from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.views import View

from cursos.models import Curso
from usuarios.models import User


class Asistencia_GralView(LoginRequiredMixin, View):
    login_url = 'usuarios:login'
    redirect_field_name = ''

    def get(self, request, **kwargs):
        curso_id = kwargs['curso_id']
        curso = get_object_or_404(Curso, pk=curso_id)
        usuaria = User.objects.get(username=request.user.username)
        if usuaria.es_profesora:
            cursos = Curso.objects.filter(profesoras__in=[usuaria])
        elif usuaria.es_voluntaria:
            cursos = Curso.objects.filter(voluntarias__in=[usuaria])

        if curso in list(cursos):
            return render(request, 'asistencia/asistencia_gral.html', {
                'curso': curso
        })
        return HttpResponseForbidden("No tienes permiso para acceder a la asistencia de este curso.")

'''
class AsistenciaView(LoginRequiredMixin, View):
    login_url = 'usuarios:login'
    redirect_field_name = ''

    def get(self, request, **kwargs):
        curso_id = kwargs['curso_id']
        curso = get_object_or_404(Curso, pk=curso_id)
        usuaria = User.objects.get(username=request.user.username)
        if usuaria.es_profesora:
            cursos = Curso.objects.filter(profesoras__in=[usuaria])
        elif usuaria.es_voluntaria:
            cursos = Curso.objects.filter(voluntarias__in=[usuaria])

        if curso in list(cursos):
            return render(request, 'asistencia/asistencia.html', {
                'curso': curso,
        })
        return HttpResponseForbidden("No tienes permiso para acceder a la asistencia de este curso.")
'''