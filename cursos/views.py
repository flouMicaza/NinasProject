from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.views import View

from cursos.models import Curso
from usuarios.models import User


class CursoView(LoginRequiredMixin, View):
    login_url = 'usuarios:login'
    redirect_field_name = ''

    def get(self, request, **kwargs, ):
        curso = get_object_or_404(Curso, pk=kwargs['curso_id'])
        return render(request, 'cursos/inicio_curso.html', {
            'curso': curso
        })


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
        usuaria = User.objects.get(username=username)
        if usuaria.es_profesora:
            cursos = Curso.objects.filter(profesoras__in=[usuaria])
        else:
            cursos = Curso.objects.filter(voluntarias__in=[usuaria])
        return list(cursos)


class EstadisticasView(LoginRequiredMixin, View):
    login_url = 'usuarios:login'
    redirect_field_name = ''

    def get(self, request, **kwargs):
        mensaje = "este curso", kwargs["curso_id"]
        return HttpResponse(mensaje)
