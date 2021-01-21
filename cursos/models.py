from django.db import models
import datetime

# Create your models here.
from usuarios.models import User
from coordinacion.models import Sede

class Tema(models.Model):
    nombre = models.CharField(max_length=50)


class Curso(models.Model):
    class Meta:
        unique_together = (('nombre', 'anho', 'sede'),)

    nombre = models.CharField(max_length=100, default="curso_default")
    profesoras = models.ManyToManyField(User, related_name="profesoras", blank=True)
    voluntarias = models.ManyToManyField(User, related_name="voluntarias", blank=True)
    alumnas = models.ManyToManyField(User, related_name="alumnas", blank=True)
    tema = models.ManyToManyField(Tema, related_name="tags", blank=True)
    cant_clases = models.IntegerField(default=1)
    anho = models.IntegerField(default=datetime.datetime.now().year)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, to_field="nombre", blank=True, null=True)

    def __str__(self):
        return self.nombre

