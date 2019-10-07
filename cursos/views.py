from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views import View

from cursos.models import Curso
from usuarios.models import User


class CursoView(LoginRequiredMixin, View):
    login_url = 'usuarios:login'
    redirect_field_name = ''

    def get(self, request, **kwargs,):
        if request.user.es_profesora or request.user.es_voluntaria:
            # return HttpResponseRedirect(reverse('cursos:mis_cursos'))
            pass
        else:
            return render(request,'cursos/inicio_curso.html')

    '''def get(self):
        #como conseguir los parametros que mando por url.
        self.kwargs['curso_id']'''


class MisCursosView(LoginRequiredMixin, View):
    login_url = 'usuarios:login'
    redirect_field_name = ''

    def get(self, request):
        if request.user.es_alumna:
            return HttpResponseRedirect(reverse('usuarios:index'))

        else:
            cursos = self.get_cursos(request.user.username)
            return render(request, 'cursos/mis_cursos.html', {'cursos': cursos})

    def get_cursos(self, username):
        """
        Método que entrega los cursos en los que username es docente
        :param username: usuario a buscar
        :return: lista de cursos
        """
        usuaria = User.objects.filter(username=username)
        if usuaria[0].es_profesora:
            cursos = Curso.objects.filter(profesoras__in=usuaria)
        else:
            cursos = Curso.objects.filter(voluntarias__in=usuaria)
        return list(cursos)
