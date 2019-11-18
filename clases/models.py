from django.db import models
from datetime import date

# Create your models here.

from cursos.models import Curso


class Problema(models.Model):
    pass


class Clase(models.Model):
    nombre = models.CharField('nombre clase', max_length=100, unique=True, default="clase_default")
    problemas = models.ManyToManyField(Problema, related_name="profesoras", blank=True)
    publica = models.BooleanField('clase publica', default=True)
    fecha_clase = models.DateField("fecha clase", default=date.today)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)


