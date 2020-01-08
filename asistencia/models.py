from datetime import timezone
from django.db import models

class Asistencia_clase(models.Model):
    alumna = models.ForeignKey('usuarios.User', related_name='alumna' ,on_delete=models.CASCADE)
    clase = models.ForeignKey('clases.Clase', on_delete=models.CASCADE)
    curso = models.ForeignKey('cursos.Curso', on_delete=models.CASCADE)
    author = models.ForeignKey('usuarios.User', related_name='profesora' ,on_delete=models.CASCADE)  # quien paso la asistencia

    def __str__(self):
        return "{0} asistió a la clase {1}".format(self.alumna.username, self.clase.nombre)
"""
    def get_asistencia_data(self, **kwargs):
        context = super(UserPreferences, self).get_context_data(**kwargs)
        context['form1'] = Preferences.objects.all()
        return context
"""

