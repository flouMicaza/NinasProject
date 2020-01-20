from datetime import date
from django.db import models
from cursos.models import Curso

class Problema(models.Model):
    pass

class Clase(models.Model):
    nombre = models.CharField('nombre clase', max_length=100, default="clase_default")
    problemas = models.ManyToManyField(Problema, related_name="profesoras", blank=True)
    publica = models.BooleanField('clase publica', default=True)
    fecha_clase = models.DateField("fecha clase", default=date.today)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("nombre", "curso"))

    def __str__(self):
        return self.nombre