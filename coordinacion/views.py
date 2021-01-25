from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils.decorators import method_decorator
from NiñasProject.decorators import coordinadora_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import UpdateView, CreateView, FormView
from django.contrib import messages
from coordinacion.forms import UserForm


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
        form.fields['profesoras'].queryset=User.objects.filter(es_profesora=True)
        form.fields['alumnas'].queryset=User.objects.filter(es_alumna=True)
        form.fields['voluntarias'].queryset=User.objects.filter(es_voluntaria=True)
        return form

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'curso modificado')
        return HttpResponseRedirect(reverse('coordinacion:cursos'))

class CoordinadoraCrearCursosView(LoginRequiredMixin, CreateView):
    model = Curso
    fields = ('nombre', 'profesoras', 'voluntarias', 'alumnas')
    template_name = 'coordinacion/cursos/crear_curso.html'
    context_object_name = 'curso'

    def get_form(self):
        form = super().get_form()
        form.fields['nombre'].initial = ""
        form.fields['profesoras'].queryset=User.objects.filter(es_profesora=True)
        form.fields['alumnas'].queryset=User.objects.filter(es_alumna=True)
        form.fields['voluntarias'].queryset=User.objects.filter(es_voluntaria=True)
        return form
    
    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('coordinacion:cursos'))


@coordinadora_required
def eliminar_curso(request, curso_id):
    Curso.objects.get(id=curso_id).delete()
    return HttpResponseRedirect(reverse('coordinacion:cursos'))

#USERS VIEWS

class CoordinadoraUsersView(LoginRequiredMixin, View):
    @method_decorator([coordinadora_required])
    def get(self, request):
        profesoras=User.objects.filter(es_profesora=True)
        alumnas=User.objects.filter(es_alumna=True)
        voluntarias=User.objects.filter(es_voluntaria=True)
        return render(request, 'coordinacion/users/users_index.html', {'profesoras':profesoras, 'alumnas':alumnas, 'voluntarias':voluntarias})

class CoordinadoraEditarUsersView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'username')
    template_name = 'coordinacion/users/editar_user.html'
    pk_url_kwarg = 'user_id'
    context_object_name = 'user'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'usuario modificado')
        return HttpResponseRedirect(reverse('coordinacion:users'))

class CoordinadoraCrearUserView(LoginRequiredMixin, FormView):
    form_class = UserForm
    template_name = 'coordinacion/users/crear_user.html'

    def form_valid(self, form):
        data = form.cleaned_data
        user = User.objects.create_user(first_name=data['first_name'], last_name=data['last_name'], username=data['username'],
               password='tempPass21', es_profesora=data['es_profesora'], es_alumna=data['es_alumna'], es_voluntaria=data['es_voluntaria'])
        user.save()
        for curso_id in data['cursos']:
            if data['es_profesora']:
                Curso.objects.get(id=int(curso_id)).profesoras.add(user)
            if data['es_voluntaria']:
                Curso.objects.get(id=int(curso_id)).voluntarias.add(user)
            if data['es_alumna']:
                Curso.objects.get(id=int(curso_id)).alumnas.add(user)

        return HttpResponseRedirect(reverse('coordinacion:users'))

@coordinadora_required
def eliminar_user(request, user_id):
    Curso.objects.get(id=user_id).delete()
    return HttpResponseRedirect(reverse('coordinacion:users'))

@coordinadora_required
def eliminar_users(request):
    users_id = request.POST.getlist('user_delete')
    for user_id in users_id:
        User.objects.get(id=user_id).delete()
    messages.success(request, 'Usuarias eliminadas')
    return HttpResponseRedirect(reverse('coordinacion:users'))
