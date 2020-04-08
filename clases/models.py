from datetime import date
from django.db import models
from cursos.models import Curso
from problemas.models import Problema


class Clase(models.Model):
    nombre = models.CharField('nombre clase', max_length=100)
    publica = models.BooleanField('clase publica', default=True,help_text="Determina si la clase estará pública para estudiantes y voluntarias")
    fecha_clase = models.DateField("fecha clase",unique=True, help_text="Fecha en la que se realizará la clase")
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, help_text="Curso al que pertenece la clase")
    problemas = models.ManyToManyField(Problema, help_text="Problemas a resolver en esta clase")
    class Meta:
        unique_together = (("nombre", "curso"))

    def __str__(self):
        return self.nombre + ' , ' + self.curso.nombre

    class Meta:
        ordering = ['fecha_clase']