from django.forms import ModelForm

from django.forms.widgets import CheckboxInput
from django.core.exceptions import ValidationError

from cursos.models import Curso
from usuarios.models import User

from django import forms


class UserForm(ModelForm):
    # todos_cursos = [(c.id, c.nombre) for c in Curso.objects.all()]
    # cursos = forms.MultipleChoiceField(choices = todos_cursos, required=False)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'es_profesora','es_alumna','es_voluntaria']
