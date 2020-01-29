from datetime import datetime
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.http import HttpResponseRedirect
from django.forms import formset_factory, modelformset_factory

from .models import Asistencia
from clases.models import Clase
from cursos.models import Curso
from usuarios.models import User
from .forms import AsistenciaForm
from .utils import *



class Asistencia_GralView(LoginRequiredMixin, View):
    login_url = 'usuarios:login'
    redirect_field_name = ''

    ## Devuelve un lista compuesta ṕor listas, hay una sublista por alumna.
    ## Cada sublista contiene a la alumna, una lista de booleanos que indica si fue
    # o no a la clase, y el nro total de clases a las que la alumna asistio
    def get_asistencias(self, asistencias, alumnas):
        alum_por_nombre = alumnas.order_by('first_name')
        nro_alumnas = len(alumnas)
        lista_asistencias = []
        i = 0

        while (len(lista_asistencias) < nro_alumnas):
            name = alum_por_nombre[i].first_name
            alum = alumnas.filter(first_name=name).order_by('last_name')

            for alumna in alum:
                asist = asistencias.filter(alumna=alumna).order_by('id')
                lista_a = []
                for asistencia in asist:
                    lista_a += [asistencia.asistio]
                total = len( asist.filter(asistio=True) )
                lista = [alumna, lista_a, total]
                lista_asistencias += [lista]
                i += 1

        return lista_asistencias


    def get(self, request, **kwargs):
        curso_id = kwargs['curso_id']
        usuaria = User.objects.get(username=request.user.username)
        curso = get_cursos(usuaria, curso_id)

        if curso != None and not usuaria.es_alumna:
            clases_totales = Clase.objects.filter(curso=curso).order_by('id')
            asistencias = Asistencia.objects.filter(clase__curso=curso).order_by('clase_id')
            lista_asistencias = list(self.get_asistencias(asistencias, curso.alumnas.all()))
            clases_asist = []             # clases que ya tienen asistencias hasta el momento
            total_por_clase = []    # total de alumnas por clase en clases

            for asistencia in asistencias:
                if not asistencia.clase in clases_asist:
                    clases_asist += [asistencia.clase]
            for clase in clases_asist:
                total_clase = len(asistencias.filter(clase=clase, asistio=True))
                total_por_clase += [total_clase]

            hay_clases = True
            if len(Clase.objects.filter(curso=curso)) == 0:
                hay_clases = not hay_clases
            hay_alumnas = True
            if len(curso.alumnas.all()) == 0:
                hay_alumnas = not hay_alumnas

            id_prox_clase = -1
            if len(clases_asist) < len(clases_totales):
                id_prox_clase = clases_totales[len(clases_asist)].id

            return render(request, 'asistencia/asistencia_gral.html', {
                'curso': curso,
                'clases': clases_asist,
                'lista_asistencias': lista_asistencias,
                'total_por_clase': total_por_clase,
                'hay_clases': hay_clases,
                'hay_alumnas': hay_alumnas,
                'id_prox_clase': id_prox_clase,
                'clases_hasta_ahora': len(clases_asist)
            })

        return HttpResponseForbidden("No tienes permiso para acceder a la asistencia de este curso.")

def get_form(request,**kwargs):
    curso_id = kwargs['curso_id']
    clase_id = kwargs['clase_id']
    usuaria = User.objects.get(username=request.user.username)

    curso = get_cursos(usuaria, curso_id)       ## entrega el curso si la persona tiene acceso
    clase = get_clases(curso_id, clase_id)      ## entrega la clase si corresponde al curso

    if curso == None:
        return HttpResponseForbidden("No tienes permiso para pasar asistencia en este curso.")

    elif clase == None:
        return HttpResponseNotFound("La clase que buscas no existe.")

    else:

        lista=get_alumnas_en_orden(curso.alumnas.all())
        AsistenciaFormset = formset_factory(AsistenciaForm, extra=len(lista))
        template_name='asistencia/asistencia.html'

        if request.method=='GET':   ## cuando entro por primera vez
            formset = AsistenciaFormset(request.GET or None)
            for idx, form in enumerate(formset):
                form.fields['asistio'].label = lista[idx]
                print(form.fields['asistio'].label)
            return render(request, template_name, {
            'curso': curso,
            'clase': clase,
            'formset': formset,
            })

        elif request.method=='POST':    ## cuando pongo save
            formset=AsistenciaFormset(request.POST)
            for idx, form in enumerate(formset):
                form.fields['asistio'].label = lista[idx]
                print(form.fields['asistio'].label)
            if formset.is_valid():
                asistentes=['alumna4', 'alumna7', 'alumna9', 'alumna14', 'alumna18', 'alumna21'] #lista de users de las alumnas que asistieron para el test de usuario
                for form in formset:
                    #asistio=form.cleaned_data.get('asistio') #lo que debería leer el input del form
                    asistio=False #todas false
                    alumna=form.fields['asistio'].label

                    if alumna.username in asistentes: #las que asistieron en el test
                        asistio=True #se les marca true a mano
                    print(request.POST)
                    clase_actual=Clase.objects.filter(id=clase_id)[0]
                    Asistencia(alumna=alumna, clase= clase_actual, author= request.user, asistio=asistio).save()

                print(type(clase_actual.curso.id))
                #return redirect('asistencia:asistencia_gral')
                return HttpResponseRedirect(reverse('asistencia:asistencia_gral', kwargs={'curso_id':clase_actual.curso.id}))
