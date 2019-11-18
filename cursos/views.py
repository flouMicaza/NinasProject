from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.views import View

from clases.models import Clase
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

    """
    
    Método que entrega las clases asociadas a un curso, según el tipo de usuario. 
    :param curso: curso que se está buscando.
    :param username: usuario que está conectado. 
    """

    def get_clases(self, curso, username):
        usuaria = User.objects.get(username=username)
        if usuaria.es_profesora:
            clases = Clase.objects.filter(curso__in=[curso])
        else:
            clases = Clase.objects.filter(curso__in=[curso], publica=True)
        return list(clases)


class CursoView(CursosView):

    def get(self, request, **kwargs, ):
        curso_id = kwargs['curso_id']
        curso = get_object_or_404(Curso, pk=curso_id)
        if curso in self.get_cursos(request.user.username):
            clases = self.get_clases(curso, request.user.username)
            return render(request, 'cursos/inicio_curso.html', {
                'curso': curso,
                'clases': clases
            })
        else:
            return HttpResponseForbidden("No tienes permiso para acceder a este curso.")


class MisCursosView(CursosView):

    def get(self, request):
        if request.user.es_profesora or request.user.es_voluntaria:
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
