from django import forms
import asistencia
from asistencia.models import Asistencia, Asistentes
from usuarios.models import User
from django.forms import formset_factory, modelformset_factory



class AsistenciaForm(forms.Form):
    #class Meta():
     #   model=Asistencia
      #  fields=('alumna','asistio',)
       # labels={'alumna': 'Alumna', 'asistio':'Asistio'}
        #widgets={'alumna': forms.TextInput(attrs={
         #       'class': 'form-control',
          #      'placeholder': 'alumna '
           #     }
            #), 'asistio':forms.CheckboxInput()}
    #alumna=forms.CharField()
    asistio=forms.BooleanField( widget=forms.CheckboxInput())


AsistenciaFormset=formset_factory(AsistenciaForm, extra=3)

"""
 #fields=('alumna','asistio'), extra=3,
                                       #widgets={'alumna': forms.TextInput(attrs={
               # 'class': 'form-control',
                #'placeholder': 'alumna '
               # }
           # ), 'asistio':forms.CheckboxInput()})"""



"""
class AsistenciaNinaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = '__all__'
        widgets = {'asistencia': forms.CheckboxSelectMultiple(attrs={'class': 'mi-clase'})}
        
        asistentes = forms.MultipleChoiceField(
            required=False,
            widget=forms.CheckboxSelectMultiple,
            choices=[True],
        )
        """
