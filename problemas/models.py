import os
import json
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.core.files import File

from clases.models import Clase
from my_lib.files_wrapper import file_to_file, change_path_extension, get_file_name, check_if_file_is_valid

class Problema(models.Model):
    titulo = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(editable=False, blank=True, null=True)

    statement = models.FileField(upload_to='statements',help_text="Solo se aceptan PDF's",validators=[FileExtensionValidator(['pdf'])])

    # The source with which the statement file was created (a .zip or another compression format)
    source = models.FileField(upload_to='source', blank=True, null=True)

    tests = models.FileField(upload_to='test_files',help_text="Se aceptan formatos .csv y .json",validators=[FileExtensionValidator(['json', 'csv'])])
    clase = models.ForeignKey(Clase, blank=True, null=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """
        On save, update timestamps
        """
        if not self.id:
            self.fecha_creacion = timezone.now()
        self.updated_at = timezone.now()

        return models.Model.save(self, *args, **kwargs)

    def __str__(self):
        return self.titulo

    def get_source_name(self):
        return self.source.name.split("/")[-1]

    def get_statement_name(self):
        return self.statement.name.split("/")[-1]

    def get_tests_name(self):
        return self.tests.name.split("/")[-1]

@receiver(post_save, sender=Problema)
def create_assignment(sender, instance, created, **kwargs):
    """
    Changes the file to a json on creation

    :param sender: The model class. (Assignment)
    :param instance: The actual instance being saved.
    :param created: Boolean; True if a new record was created.
    """

    if created and instance.tests:
        # Generates paths for the new json file
        test_url = instance.tests.url[1:]
        json_tests_url = change_path_extension(test_url, 'json')

        if not check_if_file_is_valid(test_url):
            instance.tests = None
            instance.save()
            os.remove(test_url)
            print("El archivo de test no es válido")
            return

        # Passes the information from the original file to the json file
        file_to_file(test_url, json_tests_url)

        # Saves the new json file as the tests file in the instance
        f = open(json_tests_url)
        instance.tests.save(get_file_name(json_tests_url), File(f))
        f.close()

        # Deletes the old file
        os.remove(test_url)
        create_test_cases(instance)

def create_test_cases(problema):
    with open(settings.BASE_DIR + problema.tests.url, 'r') as f:
        datastore = json.load(f)

    for test_dict in datastore:  # Aquí es donde se generan los test, tengo que modificar para que reciba mi nueva info.
        caso = Caso(categoría=test_dict["Categoria"],input=test_dict["Input"],output_esperado=test_dict["Output"],problema=problema)
        caso.save()

class Caso(models.Model):
    categoría = models.TextField(help_text="Descripción del caso")
    input = models.CharField(max_length=255,help_text="Input del caso")
    output_esperado = models.CharField(max_length=255,help_text="Output esperado para el input")
    problema = models.ForeignKey(Problema, on_delete=models.CASCADE, help_text="Problema al que pertenece el caso")

    def __str__(self):
        return self.problema.titulo + "-" + str(self.id)