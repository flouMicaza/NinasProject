from django import forms
import asistencia
from asistencia.models import Asistencia, Asistentes
from usuarios.models import User


class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistentes
        fields = ('asistentes', 'clase',)
        widgets = {'asistentes': forms.CheckboxSelectMultiple,}



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
