from django.forms import ModelForm

from django.forms.widgets import CheckboxInput
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from cursos.models import Curso
from usuarios.models import User

from django import forms


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'es_profesora','es_alumna','es_voluntaria']

class CursoForm(ModelForm):
    lista_alumnas = forms.FileField(required=False, help_text="Solo se acepta formato csv",validators=[FileExtensionValidator(['json', 'csv'])])
    class Meta:
        model = Curso
        fields = ['nombre', 'profesoras', 'voluntarias', 'alumnas']