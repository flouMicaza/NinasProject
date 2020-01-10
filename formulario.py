from django import forms
from usuarios.models import User

class AsistenicaForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('preferences',)
        widgets = {'preferences': forms.CheckboxSelectMultiple(attrs={'class': 'mi-clase'})}

