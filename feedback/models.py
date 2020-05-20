from django.core.validators import FileExtensionValidator
from django.db import models

# Create your models here.
from problemas.models import Problema, Caso
from usuarios.models import User


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Usuaria dueña del feedback.")
    problema = models.ForeignKey(Problema, on_delete=models.CASCADE, help_text="Problema asociado al feedback")
    fecha_envio = models.DateTimeField(auto_now_add=True, help_text="Fecha y hora en que se recibe el feedback")
    codigo_solucion = models.FileField(upload_to='soluciones', help_text="Se acepta formato .cpp",
                                       validators=[FileExtensionValidator(['cpp'])])

    def __str__(self):
        return str(self.user) + ":" + str(self.problema)


class TestFeedback(models.Model):
    passed = models.BooleanField(help_text="Si el test paso o no")
    output_obtenido = models.CharField(max_length=255, help_text="Output obtenido para el test")
    error = models.CharField(max_length=500)
    caso = models.ForeignKey(Caso, on_delete=models.CASCADE, help_text="Caso que probó este test_feedback")
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE,
                                 help_text="Feedback con que se creó este test_feedback")


class OutputAlternativo(models.Model):
    caso = models.ForeignKey(Caso, on_delete=models.CASCADE, help_text="Caso que probó este test_feedback")
    output_obtenido = models.CharField(max_length=255, help_text="Output obtenido para el test")
    frecuencia = models.IntegerField(help_text="Frecuencia con que ha aparecido el output", default=1)
    agregado = models.BooleanField(help_text="Si se ha agregado o no como output alternativo", default=False)

    class Meta:
        unique_together = ("caso", "output_obtenido")

