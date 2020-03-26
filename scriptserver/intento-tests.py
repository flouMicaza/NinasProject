# Probar que pasa si le paso un archivo que no es cpp
# Probar que pasa si le paso un archivo cpp malo
# Probar que pasa si le paso un archivo cpp bueno
# Probar que pasa si evaluo 5 códigos
# Probar que pasa si evaluo 10 códigos
# Probar que pasa si evaluo 20 códigos
# Probar que pasa si evaluo 40 códigos
import os

from django.core.files.storage import FileSystemStorage
from django.test import TestCase, Client

from problemas.models import Problema
from scriptserver.comunication.client import Client

ComunicationClient = Client()

class scriptServerTest(TestCase):
    def setUp(self):
        fs = FileSystemStorage()
        enunciado = 'statements/Problem_-_4A_-_Codeforces.pdf'
        tests = 'test_files/testCases_JSfqHcL.json'
        self.problema = Problema.objects.create(titulo="Problema de prueba",statement=enunciado,tests=tests)
        self.test_path = self.problema.tests.path.replace("\\", "/")

    def test_solucion_resultado_correcto(self):
        script_path = '/home/flourensia/Documents/Memoria/NinasProject/media/solucion_cpp_buena.cpp'
        response = ComunicationClient.send_submission(script_path, self.test_path, 'cpp')
        self.assertEqual(response[0],'success')