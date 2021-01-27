from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils.decorators import method_decorator
from NiñasProject.decorators import coordinadora_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import UpdateView, CreateView, FormView
from django.contrib import messages
from coordinacion.forms import UserForm, CursoForm
from django.core.exceptions import ValidationError
from my_lib.files_wrapper import check_valid_csv_users
#from usuarios.management.commands.crear_users import Command

import csv
import datetime

from coordinacion.models import Sede
from cursos.models import Curso
from usuarios.models import User
# Create your views here.
from django.views import View


class CoordinadoraInicioView(LoginRequiredMixin, View):
    @method_decorator([coordinadora_required])
    def get(self, request):
        return render(request, 'coordinacion/inicio_coordinadora.html')

# CURSOS VIEWS
class CoordinadoraCursosView(LoginRequiredMixin, View):
    @method_decorator([coordinadora_required])
    def get(self, request):
        cursos = Curso.objects.all()
        return render(request, 'coordinacion/cursos/cursos.html', {'cursos':cursos})


class CoordinadoraEditarCursosView(LoginRequiredMixin, UpdateView):
    model = Curso
    fields = ('nombre', 'profesoras', 'voluntarias', 'alumnas')
    template_name = 'coordinacion/cursos/editar_curso.html'
    pk_url_kwarg = 'curso_id'
    context_object_name = 'curso'

    def get_form(self):
        form = super().get_form()
        sede = Sede.objects.get(coordinadora=self.request.user)
        form.fields['profesoras'].queryset = sede.profesoras.filter(es_profesora=True, is_active=True)
        form.fields['alumnas'].queryset = sede.alumnas.filter(es_alumna=True, is_active=True)
        form.fields['voluntarias'].queryset = sede.voluntarias.filter(es_voluntaria=True, is_active=True)
        return form

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Curso modificado')
        return HttpResponseRedirect(reverse('coordinacion:cursos'))

class CoordinadoraCrearCursosView(LoginRequiredMixin, CreateView):
    # model = Curso
    # fields = ('nombre', 'sede', 'profesoras', 'voluntarias', 'alumnas')
    template_name = 'coordinacion/cursos/crear_curso.html'
    context_object_name = 'curso'

    def get_form(self):
        form = CursoForm()
        sede = Sede.objects.get(coordinadora=self.request.user)
        form.fields['nombre'].initial = ""
        form.fields['profesoras'].queryset = sede.profesoras.filter(es_profesora=True, is_active=True)
        form.fields['alumnas'].queryset = sede.alumnas.filter(es_alumna=True, is_active=True)
        form.fields['voluntarias'].queryset = sede.voluntarias.filter(es_voluntaria=True, is_active=True)
        return form

    def post(self, request, *args, **kwargs):
        try:
            self.validate(request)
        except Exception as e:
            messages.success(request, e)
            return HttpResponseRedirect(reverse('coordinacion:crear_curso'))
        self.form_valid(request)
        messages.success(self.request, 'Curso creado')
        return HttpResponseRedirect(reverse('coordinacion:cursos'))


    def validate(self, request):
        user = request.user
        form = request.POST
        sede = Sede.objects.get(coordinadora=user)
        if len(Curso.objects.filter(nombre=form['nombre'], anho = datetime.datetime.now().year, sede=sede.nombre))>0:
            raise ValidationError("Ya existe un curso con este nombre este año en esta sede")
        lista = request.FILES['lista_alumnas']
        check_valid_csv_users(lista)
        
    def form_valid(self, request):
        form = request.POST
        user = request.user
        sede = Sede.objects.get(coordinadora=user)
        curso = Curso.objects.create(nombre=form.get('nombre'), sede=sede)
        for profesora in form.getlist('profesoras'):
            curso.profesoras.add(profesora)
        for alumna in form.getlist('alumnas'):
            curso.alumnas.add(alumna)
        for voluntaria in form.getlist('voluntarias'):
            curso.voluntarias.add(voluntaria)
        curso.save()


@coordinadora_required
def eliminar_curso(request, curso_id):
    Curso.objects.get(id=curso_id).delete()
    return HttpResponseRedirect(reverse('coordinacion:cursos'))

@coordinadora_required
def eliminar_cursos(request):
    cursos_id = request.POST.getlist('cursos_delete')
    for curso_id in cursos_id:
        Curso.objects.get(id=curso_id).delete()
    messages.success(request, 'Cursos eliminados')
    return HttpResponseRedirect(reverse('coordinacion:cursos'))

#USERS VIEWS

class CoordinadoraUsersView(LoginRequiredMixin, View):
    @method_decorator([coordinadora_required])
    def get(self, request):
        sede = Sede.objects.get(coordinadora=self.request.user)
        profesoras = sede.profesoras.filter(es_profesora=True, is_active=True)
        alumnas = sede.alumnas.filter(es_alumna=True, is_active=True)
        voluntarias = sede.voluntarias.filter(es_voluntaria=True, is_active=True)
        return render(request, 'coordinacion/users/users_index.html', {'profesoras':profesoras, 'alumnas':alumnas, 'voluntarias':voluntarias})

class CoordinadoraEditarUsersView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'es_alumna', 'es_voluntaria', 'es_profesora')
    template_name = 'coordinacion/users/editar_user.html'
    pk_url_kwarg = 'user_id'
    context_object_name = 'user'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Usuaria modificada')
        return HttpResponseRedirect(reverse('coordinacion:users'))

class CoordinadoraCrearUserView(LoginRequiredMixin, FormView):
    form_class = UserForm
    template_name = 'coordinacion/users/crear_user.html'

    def form_valid(self, form):
        data = form.cleaned_data
        user = User.objects.create_user(first_name=data['first_name'], last_name=data['last_name'], username=data['username'],
               password='tempPass21', es_profesora=data['es_profesora'], es_alumna=data['es_alumna'], es_voluntaria=data['es_voluntaria'])
        user.save()
        sede = Sede.objects.get(coordinadora=self.request.user)
        if data['es_profesora']:
            sede.profesoras.add(user)
        if data['es_voluntaria']:
            sede.voluntarias.add(user)
        if data['es_alumna']:
            sede.alumnas.add(user)
        messages.success(self.request, 'Usuaria Creada')
        return HttpResponseRedirect(reverse('coordinacion:users'))

@coordinadora_required
def eliminar_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = False
    user.save()
    return HttpResponseRedirect(reverse('coordinacion:users'))

@coordinadora_required
def eliminar_users(request):
    users_id = request.POST.getlist('user_delete')
    for user_id in users_id:
        user = User.objects.get(id=user_id)
        user.is_active = False
        user.save()
    messages.success(request, 'Usuarias eliminadas')
    return HttpResponseRedirect(reverse('coordinacion:users'))
