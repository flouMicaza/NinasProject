from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from NiñasProject.decorators import *
#
from NiñasProject.utils import get_cursos
from clases.forms import ClaseForm
from django.contrib import messages

@method_decorator([profesora_required], name='dispatch')
class CrearClaseView(LoginRequiredMixin, View):
    login_url = 'usuarios:login'
    redirect_field_name = ''

    def get(self,request, **kwargs):
        curso_id = kwargs['curso_id']
        curso = get_cursos(request.user, curso_id)

        if curso == None:
            return HttpResponseForbidden("No tienes permiso para ingresar a este curso.")

        form = ClaseForm()
        return render(request, 'clases/crear_clase.html', {'curso': curso, 'form': form})


    def post(self,request,**kwargs):
        curso_id = kwargs['curso_id']
        curso = get_cursos(request.user, curso_id)
        form = ClaseForm(request.POST)
        if form.is_valid():
            nueva_clase = form.save()
            messages.success(request, 'Se creó la clase ' + nueva_clase.nombre)
            return HttpResponseRedirect(reverse('cursos:curso', kwargs=kwargs))
        return render(request, 'clases/crear_clase.html', {'curso':curso, 'form':form})