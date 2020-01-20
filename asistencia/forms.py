from django import forms
import asistencia
from asistencia.models import Asistencia, Asistentes
from usuarios.models import User
from django.forms import formset_factory, modelformset_factory


class AsistenciaForm(forms.Form):
    asistio=forms.BooleanField(required=False, widget=forms.CheckboxInput())

    def clean(self):
        print('cleaneando')
        return super(forms.Form,self).clean()

    '''def __init__(self, *args, **kwargs):
        super(AsistenciaForm,self).__init__(*args,**kwargs)'''

AsistenciaFormset = formset_factory(AsistenciaForm)