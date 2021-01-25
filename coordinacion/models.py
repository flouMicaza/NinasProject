from django.db import models

# Create your models here.
class Sede(models.Model):
    nombre = models.CharField(max_length=100, default="Sede", primary_key=True)

    def __str__(self):
        return self.nombre