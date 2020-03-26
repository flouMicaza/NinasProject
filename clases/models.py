from datetime import date
from django.db import models
from cursos.models import Curso
from problemas.models import Problema


class Clase(models.Model):
    nombre = models.CharField('nombre clase', max_length=100, default="clase_default")
    publica = models.BooleanField('clase publica', default=True)
    fecha_clase = models.DateField("fecha clase", default=date.today)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    problemas = models.ManyToManyField(Problema)
    class Meta:
        unique_together = (("nombre", "curso"))

    def __str__(self):
        return self.nombre + ' , ' + self.curso.nombre
