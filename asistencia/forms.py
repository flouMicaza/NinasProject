from django import forms
import asistencia
from asistencia.models import Asistencia, Asistentes
from usuarios.models import User
from django.forms import formset_factory, modelformset_factory


class AsistenciaForm(forms.Form):
    asistio=forms.BooleanField(label='hola', widget=forms.CheckboxInput())

    def __init__(self, *args, **kwargs):
        super(AsistenciaForm,self).__init__(*args,**kwargs)