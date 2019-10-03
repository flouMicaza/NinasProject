from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import never_cache


class IndexView(LoginRequiredMixin, View):
    login_url = 'usuarios:login'
    redirect_field_name = ''

    def get(self, request):
        if request.user.es_profesora or request.user.es_voluntaria:
            return render(request,'cursos/inicio_docente.html')
        else:
            return render(request, 'cursos/inicio_curso.html')


class LoginView(View):

    @never_cache
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('usuarios:index'))
        return render(request, 'registration/login.html')

    def post(self, request):

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect(reverse('usuarios:index'))
        else:
            # Return an 'invalid login' error message.
            return render(request, 'registration/login.html', {
                'error_message': 'Usuario o contraseña incorrectos'
            })


class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('usuarios:index'))
