from django.forms import ModelForm, HiddenInput, ModelMultipleChoiceField
from clases.models import Clase
from cursos.models import Curso



from django.contrib.admin.widgets import AdminFileWidget
from django.forms.widgets import HiddenInput, FileInput


class HTML5RequiredMixin(object):

    def __init__(self, *args, **kwargs):
        super(HTML5RequiredMixin, self).__init__(*args, **kwargs)
        for field in self.fields:
            if (self.fields[field].required and
               type(self.fields[field].widget) not in
                    (AdminFileWidget, HiddenInput, FileInput) and
               '__prefix__' not in self.fields[field].widget.attrs):

                    self.fields[field].widget.attrs['required'] = 'required'
                    if self.fields[field].label:
                        self.fields[field].label += ' *'


class ClaseForm(HTML5RequiredMixin,ModelForm):

    class Meta:
        model = Clase
        exclude = ['problemas']

