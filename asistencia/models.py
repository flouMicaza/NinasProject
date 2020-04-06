from datetime import timezone
from django.db import models

from usuarios.models import User


class Asistencia(models.Model):
    alumna = models.ForeignKey('usuarios.User', related_name='alumna' ,on_delete=models.CASCADE)
    clase = models.ForeignKey('clases.Clase', on_delete=models.CASCADE)
    asistio = models.BooleanField('alumna asisitio', default=False)



    class Meta:
        unique_together=(("alumna","clase"))

    def __str__(self):
        if self.asistio:
            return "{0} asistió a la clase {1}".format(self.alumna.username, self.clase.nombre)
        return "{0} NO asistió a la clase {1}".format(self.alumna.username, self.clase.nombre)

