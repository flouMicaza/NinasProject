from django.forms import ModelForm

from django.contrib.admin.widgets import AdminFileWidget
from django.forms.widgets import HiddenInput, FileInput

from problemas.models import Problema


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


class ProblemaForm(HTML5RequiredMixin,ModelForm):

    class Meta:
        model = Problema
        exclude = ['source', 'fecha_creacion']