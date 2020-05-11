# Probar que pasa si le paso un archivo que no es cpp
# Probar que pasa si le paso un archivo cpp malo
# Probar que pasa si le paso un archivo cpp bueno
# Probar que pasa si evaluo 5 códigos
# Probar que pasa si evaluo 10 códigos
# Probar que pasa si evaluo 20 códigos
# Probar que pasa si evaluo 40 códigos
import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.test import TestCase, Client

from problemas.models import Problema
from scriptserver.comunication.client import Client
from shutil import copyfile

ComunicationClient = Client()

class scriptServerTest(TestCase):
    def setUp(self):
        fs = FileSystemStorage()
        enunciado = 'test/Problem_-_4A_-_Codeforces.pdf'
        tests = settings.MEDIA_ROOT + '/test/casos_test.json'
        new_test= 'new_test.json'
        new_test1 = copyfile(tests,settings.MEDIA_ROOT+ '/' + new_test)
        self.problema = Problema.objects.create(titulo="Problema de prueba",statement=enunciado,tests=new_test)
        self.test_path = self.problema.tests.path.replace("\\", "/")

    def test_solucion_resultado_correcto(self):
        script_path = settings.MEDIA_ROOT + '/test/watermelon.cpp'
        response = []
        for i in range(2):
            repsonse1 = ComunicationClient.send_submission(script_path, self.test_path, 'cpp')
            response.append(repsonse1)
        self.assertEqual(response[0][0],'success')
        self.assertEqual(response[1][0], 'success')