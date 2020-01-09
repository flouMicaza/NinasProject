from datetime import datetime
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View

from .models import Asistencia
from asistencia.forms import AsistenciaForm
from clases.models import Clase
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
        clases = Clase.objects.filter(curso=curso)

        if curso in list(cursos):
            return render(request, 'asistencia/asistencia_gral.html', {
                'curso': curso,
                'clases': clases,
        })
        return HttpResponseForbidden("No tienes permiso para acceder a la asistencia de este curso.")


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
        clase = Clase.objects.filter(curso=curso, fecha_clase__in=[datetime.today()])
        form = self.get_form(request)

        if curso in list(cursos):
            return render(request, 'asistencia/asistencia.html', {
                'curso': curso,
                'clase': clase,
                'form': form
        })

        return HttpResponseForbidden("No tienes permiso para acceder a la asistencia de este curso.")

    def get_form(self, request):
        if request.method == "POST":
            form = AsistenciaForm(request.POST)
            asistentes = form.save(commit=False)
            asistentes.author=request.user
            asistentes.guardarAsistencia()
        else:
            form = AsistenciaForm()
        return form









