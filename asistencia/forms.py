from django import forms
import asistencia
from asistencia.models import Asistencia, Asistentes
from usuarios.models import User
from django.forms import formset_factory, modelformset_factory
from django.forms import modelformset_factory


class AsistenciaForm(forms.Form):
    asistio=forms.BooleanField(required=False, widget=forms.CheckboxInput())

    def clean(self):
        print("--------------CLEAN")
        print('cleaneando')
        return super(forms.Form,self).clean()

    '''def __init__(self, *args, **kwargs):
        super(AsistenciaForm,self).__init__(*args,**kwargs)'''



AsistenciaModelFormSet = modelformset_factory(
    Asistencia,
    fields=('asistio', ),
    widgets={'asistio': forms.CheckboxInput()}
)