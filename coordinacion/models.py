from django.db import models

# Create your models here.
from usuarios.models import User


class Sede(models.Model):
    nombre = models.CharField(max_length=100, default="Sede", primary_key=True)
    profesoras = models.ManyToManyField(User, related_name="sedes_profesoras", blank=True)
    voluntarias = models.ManyToManyField(User, related_name="sedes_voluntarias", blank=True)
    alumnas = models.ManyToManyField(User, related_name="sedes_alumnas", blank=True)
    coordinadora = models.ForeignKey(User, related_name="sedes_coordinadora", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.nombre