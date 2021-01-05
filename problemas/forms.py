from django.forms import ModelForm

from django.contrib.admin.widgets import AdminFileWidget
from django.forms.widgets import HiddenInput, FileInput

from problemas.models import Problema


class ProblemaForm(ModelForm):
    class Meta:
        model = Problema
        exclude = ['source', 'fecha_creacion', 'clase']
