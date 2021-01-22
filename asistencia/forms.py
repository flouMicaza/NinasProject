from django import forms
import asistencia
from asistencia.models import Asistencia
from usuarios.models import User
from django.forms import formset_factory, modelformset_factory
from django.forms import modelformset_factory
from django.forms.widgets import CheckboxInput




AsistenciaModelFormSet = modelformset_factory(
    Asistencia,
    fields=('asistio', ), extra=0,
    widgets = {'asistio': CheckboxInput(attrs={"Yes":True, "No":False})}
)
