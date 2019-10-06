from django.db import models

# Create your models here.
from usuarios.models import User


class Tema(models.Model):
    nombre = models.CharField(max_length=50)


class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    profesoras = models.ManyToManyField(User, related_name="profesoras", blank=True)
    voluntarias = models.ManyToManyField(User, related_name="voluntarias", blank=True)
    alumnas = models.ManyToManyField(User, related_name="alumnas", blank=True)
    tema = models.ManyToManyField(Tema, related_name="tags", blank=True)

