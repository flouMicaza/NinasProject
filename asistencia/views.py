from datetime import datetime
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.http import HttpResponseRedirect
from django.forms import formset_factory

from .models import Asistencia
from asistencia.forms import AsistenciaFormset
from clases.models import Clase
from cursos.models import Curso
from usuarios.models import User
from .forms import AsistenciaForm


class Asistencia_GralView(LoginRequiredMixin, View):
    login_url = 'usuarios:login'
    redirect_field_name = ''

    ## devuelve un diccionario que tiene como llave a la alumna del curso y como valor una lista con las clases a las que asistio
    def get_asistencias(self, asistencias, alumnas):
        lista_alumnas = []
        lista_clases = []
        # asist_por_nombre = asistencias.order_by('alumna__first_name')
        alum_por_nombre = alumnas.order_by('first_name')
        nro_alumnas = len(alumnas)

        i = 0

        while (len(lista_alumnas) < nro_alumnas):
            name = alum_por_nombre[i].first_name
            alum = alumnas.filter(first_name=name).order_by('last_name')

            for alumna in alum:
                print("alumna = ", alumna)
                asist = asistencias.filter(alumna=alumna)
                lista = []
                index = 0
                while (len(lista) < len(asist)):
                    lista += [asist[index].clase]
                    index += 1

                lista_alumnas += [alumna]
                lista_clases += [lista]
                i += 1

        return [lista_alumnas, lista_clases]


    def get(self, request, **kwargs):
        curso_id = kwargs['curso_id']
        curso = get_object_or_404(Curso, pk=curso_id)
        usuaria = User.objects.get(username=request.user.username)
        if usuaria.es_profesora:
            curso = Curso.objects.filter(profesoras__in=[usuaria], id=curso_id)
        elif usuaria.es_voluntaria:
            curso = Curso.objects.filter(voluntarias__in=[usuaria], id=curso_id)

        if len(list(curso))>0:
            curso = curso[0]

            clases = Clase.objects.filter(curso=curso)
            asistencias = Asistencia.objects.filter(clase__curso=curso)

            lista = self.get_asistencias(asistencias, curso.alumnas.all())
            lista_alumnas = lista[0]
            lista_clases = lista[1]

            return render(request, 'asistencia/asistencia_gral.html', {
                'curso': curso,
                'clases': clases,
                'alumnas' : lista_alumnas,
                'asistencias': lista_clases
        })
        return HttpResponseForbidden("No tienes permiso para acceder a la asistencia de este curso.")


class AsistenciaView(LoginRequiredMixin, View):
    login_url = 'usuarios:login'
    redirect_field_name = ''

    def get(self, request, **kwargs):
        curso_id = kwargs['curso_id']
        clase_id = kwargs['clase_id']
        curso = get_object_or_404(Curso, pk=curso_id)
        usuaria = User.objects.get(username=request.user.username)
        if usuaria.es_profesora:
            cursos = Curso.objects.filter(profesoras__in=[usuaria])
        elif usuaria.es_voluntaria:
            cursos = Curso.objects.filter(voluntarias__in=[usuaria])
        else:
            return HttpResponseForbidden("No tienes permiso para acceder a la asistencia de este curso.")

        clase = list(Clase.objects.filter(curso=curso, id=clase_id))[0]
        form = self.get_form(request)

        if curso in list(cursos):
            return render(request, 'asistencia/asistencia.html', {
                'curso': curso,
                'clase': clase,
                'form': form
        })

        return HttpResponseForbidden("No tienes permiso para acceder a la asistencia de este curso.")

def get_form(request,**kwargs):
    template_name='asistencia/asistencia.html'
    heading_message = 'Model Formset Demo'
    if request.method=='GET':
        formset=AsistenciaFormset(queryset=Asistencia.objects.none())
    elif request.method=='POST':
        formset=AsistenciaFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                print("alumna form", form.cleaned_data.get('alumna'))
            #return redirect('asistencia:asistencia_gral')
            return HttpResponseRedirect(reverse('asistencia:asistencia_gral', {'curso_id':1}))
    return render(request,template_name,{'formset':formset,'heading': heading_message,})




