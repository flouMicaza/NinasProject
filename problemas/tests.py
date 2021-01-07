import datetime
import base64
from django.test import TestCase, Client, LiveServerTestCase
from django.core.files.uploadedfile import SimpleUploadedFile, InMemoryUploadedFile
from io import BytesIO

# Create your tests here.
from django.urls import reverse

from clases.models import Clase
from cursos.models import Curso
from usuarios.models import User
from problemas.models import Problema

class InitialData(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuaria_profesora = User.objects.create_user(username="profesora", password="contraseña123",
                                                          es_profesora=True)

        self.curso_basico = Curso.objects.create(nombre="C++: Básico")
        self.curso_basico.profesoras.add(self.usuaria_profesora)
        self.clase_basica_1 = Clase.objects.create(nombre="Variables", curso=self.curso_basico, publica=True,
                                                   fecha_clase=datetime.date(2019, 10, 19))


class SubirArchivosTestJSON(InitialData):
    # probar que al cargar un curso se ven sus clases asociadas.
    def setUp(self):
        super(SubirArchivosTestJSON, self).setUp()
    
    '''Al ser el test correcto, se crean muchos archivos

    def test_no_problem(self):
        self.client.force_login(user=self.usuaria_profesora)
        titulo = 'ProblemaTEST'
        statement = SimpleUploadedFile('statement.pdf', b'a', 'application/pdf')
        tests = b'[{\n    "Input":"2020", \n    "Output": "Si\\n", \n    "Categoria": "Anno multiplo de 4"}]'
        tests = InMemoryUploadedFile(BytesIO(tests), 'tests', 'tests.json', 'application/json', len(tests), None, None)
        form_data = {
            'titulo':titulo,
            'statement':statement,
            'tests':tests
        }
        response = self.client.post(reverse('problemas:crear-problema', kwargs={'clase_id': self.clase_basica_1.id}), data = form_data, follow = True)
        self.assertContains(response, titulo)
        response = self.client.get(reverse('problemas:casos-problema', kwargs={'curso_id':self.curso_basico.id, 'problema_id': Problema.objects.first().id, 'result':0}))
        self.assertContains(response, "2020")
        self.assertContains(response, "Anno multiplo de 4")'''
    

    def test_same_input_problem(self):
        self.client.force_login(user=self.usuaria_profesora)
        titulo = 'ProblemaTEST'
        statement = SimpleUploadedFile('statement.pdf', b'a', 'application/pdf')
        tests = b'[{\n    "Input":"2020", \n    "Output": "Si\\n", \n    "Categoria": "Anno multiplo de 4"},\n {\n    "Input":"2020", \n    "Output": "Si\\n", \n    "Categoria": "Anno multiplo de 4"}]'
        tests = InMemoryUploadedFile(BytesIO(tests), 'tests', 'tests.json', 'application/json', len(tests), None, None)
        form_data = {
            'titulo':titulo,
            'statement':statement,
            'tests':tests
        }
        response = self.client.post(reverse('problemas:crear-problema', kwargs={'clase_id': self.clase_basica_1.id}), data = form_data, follow = True)
        assert len(Problema.objects.all()) == 0
        self.assertContains(response, 'El input &quot;2020&quot; se repite en los test 1 y 2')
    
    def test_less_headers(self):
        self.client.force_login(user=self.usuaria_profesora)
        titulo = 'ProblemaTEST'
        statement = SimpleUploadedFile('statement.pdf', b'a', 'application/pdf')
        tests = b'[{\n    "Input":"2020", \n    "Output": "Si\\n"}]'
        tests = InMemoryUploadedFile(BytesIO(tests), 'tests', 'tests.json', 'application/json', len(tests), None, None)
        form_data = {
            'titulo':titulo,
            'statement':statement,
            'tests':tests
        }
        response = self.client.post(reverse('problemas:crear-problema', kwargs={'clase_id': self.clase_basica_1.id}), data = form_data, follow = True)
        assert len(Problema.objects.all()) == 0
        self.assertContains(response, 'Hay menos elementos de los esperados en el test 1')
    
    def test_incorrect_header_input(self):
        self.client.force_login(user=self.usuaria_profesora)
        titulo = 'ProblemaTEST'
        statement = SimpleUploadedFile('statement.pdf', b'a', 'application/pdf')
        tests = b'[{\n    "INput":"2020", \n    "Output": "Si\\n", \n "Categoria": "Anno multiplo de 4"}]'
        tests = InMemoryUploadedFile(BytesIO(tests), 'tests', 'tests.json', 'application/json', len(tests), None, None)
        form_data = {
            'titulo':titulo,
            'statement':statement,
            'tests':tests
        }
        response = self.client.post(reverse('problemas:crear-problema', kwargs={'clase_id': self.clase_basica_1.id}), data = form_data, follow = True)
        assert len(Problema.objects.all()) == 0
        self.assertContains(response, 'El primer Header del test:1 debería ser Input, pero es INput')

    def test_incorrect_header_output(self):
        self.client.force_login(user=self.usuaria_profesora)
        titulo = 'ProblemaTEST'
        statement = SimpleUploadedFile('statement.pdf', b'a', 'application/pdf')
        tests = b'[{\n    "Input":"2020", \n    "OUtput": "Si\\n", \n "Categoria": "Anno multiplo de 4"}]'
        tests = InMemoryUploadedFile(BytesIO(tests), 'tests', 'tests.json', 'application/json', len(tests), None, None)
        form_data = {
            'titulo':titulo,
            'statement':statement,
            'tests':tests
        }
        response = self.client.post(reverse('problemas:crear-problema', kwargs={'clase_id': self.clase_basica_1.id}), data = form_data, follow = True)
        assert len(Problema.objects.all()) == 0
        self.assertContains(response, 'El segundo Header del test:1 debería ser Output, pero es OUtput')

    def test_incorrect_header_Categoria(self):
        self.client.force_login(user=self.usuaria_profesora)
        titulo = 'ProblemaTEST'
        statement = SimpleUploadedFile('statement.pdf', b'a', 'application/pdf')
        tests = b'[{\n    "Input":"2020", \n    "Output": "Si\\n", \n "CAtegoria": "Anno multiplo de 4"}]'
        tests = InMemoryUploadedFile(BytesIO(tests), 'tests', 'tests.json', 'application/json', len(tests), None, None)
        form_data = {
            'titulo':titulo,
            'statement':statement,
            'tests':tests
        }
        response = self.client.post(reverse('problemas:crear-problema', kwargs={'clase_id': self.clase_basica_1.id}), data = form_data, follow = True)
        assert len(Problema.objects.all()) == 0
        self.assertContains(response, 'El tercer Header del test:1 debería ser Categoria, pero es CAtegoria')

    def test_invalid_json(self):
        self.client.force_login(user=self.usuaria_profesora)
        titulo = 'ProblemaTEST'
        statement = SimpleUploadedFile('statement.pdf', b'a', 'application/pdf')
        tests = b'[{\n    "Input":"2020", \n    "Output": "Si\\n", \n "CAtegoria": "Anno multiplo de 4"'
        tests = InMemoryUploadedFile(BytesIO(tests), 'tests', 'tests.json', 'application/json', len(tests), None, None)
        form_data = {
            'titulo':titulo,
            'statement':statement,
            'tests':tests
        }
        response = self.client.post(reverse('problemas:crear-problema', kwargs={'clase_id': self.clase_basica_1.id}), data = form_data, follow = True)
        assert len(Problema.objects.all()) == 0
        self.assertContains(response, 'El archivo de test no es')


class SubirArchivosTestCSV(InitialData):
    # probar que al cargar un curso se ven sus clases asociadas.
    def setUp(self):
        super(SubirArchivosTestCSV, self).setUp()

    ''' Al ser el test correcto, se crean muchos archivos

    def test_no_problem(self):
        self.client.force_login(user=self.usuaria_profesora)
        titulo = 'ProblemaTEST'
        statement = SimpleUploadedFile('statement.pdf', b'a', 'application/pdf')
        tests = b'"Input","Output","Categoria"\n"2020","Si\\n","Ano multiplo de 4"'
        tests = InMemoryUploadedFile(BytesIO(tests), 'tests', 'tests.csv', 'application/csv', len(tests), None, None)
        form_data = {
            'titulo':titulo,
            'statement':statement,
            'tests':tests
        }
        response = self.client.post(reverse('problemas:crear-problema', kwargs={'clase_id': self.clase_basica_1.id}), data = form_data, follow = True)
        self.assertContains(response, titulo)
        response = self.client.get(reverse('problemas:casos-problema', kwargs={'curso_id':self.curso_basico.id, 'problema_id': Problema.objects.first().id, 'result':0}))
        self.assertContains(response, "2020")
        self.assertContains(response, "Ano multiplo de 4")'''

    def test_same_input_problem(self):
        self.client.force_login(user=self.usuaria_profesora)
        titulo = 'ProblemaTEST'
        statement = SimpleUploadedFile('statement.pdf', b'a', 'application/pdf')
        tests = b'"Input","Output","Categoria"\n"2020","Si\\n","Ano multiplo de 4"\n"2020","Si\\n","Ano multiplo de 4"'
        tests = InMemoryUploadedFile(BytesIO(tests), 'tests', 'tests.csv', 'application/csv', len(tests), None, None)
        form_data = {
            'titulo':titulo,
            'statement':statement,
            'tests':tests
        }
        response = self.client.post(reverse('problemas:crear-problema', kwargs={'clase_id': self.clase_basica_1.id}), data = form_data, follow = True)
        assert len(Problema.objects.all()) == 0
        self.assertContains(response, 'El input &quot;2020&quot; se repite en los test 1 y 2')
    
    def test_less_headers(self):
        self.client.force_login(user=self.usuaria_profesora)
        titulo = 'ProblemaTEST'
        statement = SimpleUploadedFile('statement.pdf', b'a', 'application/pdf')
        tests = b'"Input","Output"\n"2020","Si\\n"'
        tests = InMemoryUploadedFile(BytesIO(tests), 'tests', 'tests.csv', 'application/csv', len(tests), None, None)
        form_data = {
            'titulo':titulo,
            'statement':statement,
            'tests':tests
        }
        response = self.client.post(reverse('problemas:crear-problema', kwargs={'clase_id': self.clase_basica_1.id}), data = form_data, follow = True)
        assert len(Problema.objects.all()) == 0
        self.assertContains(response, 'Hay una cantidad distinta de columnas a las esperadas')
    
    def test_incorrect_header_input(self):
        self.client.force_login(user=self.usuaria_profesora)
        titulo = 'ProblemaTEST'
        statement = SimpleUploadedFile('statement.pdf', b'a', 'application/pdf')
        tests = b'"INput","Output","Categoria"\n"2020","Si\\n","Ano multiplo de 4"'
        tests = InMemoryUploadedFile(BytesIO(tests), 'tests', 'tests.csv', 'application/csv', len(tests), None, None)
        form_data = {
            'titulo':titulo,
            'statement':statement,
            'tests':tests
        }
        response = self.client.post(reverse('problemas:crear-problema', kwargs={'clase_id': self.clase_basica_1.id}), data = form_data, follow = True)
        assert len(Problema.objects.all()) == 0
        self.assertContains(response, 'El primer Header debería ser Input, pero es INput')

    def test_incorrect_header_output(self):
        self.client.force_login(user=self.usuaria_profesora)
        titulo = 'ProblemaTEST'
        statement = SimpleUploadedFile('statement.pdf', b'a', 'application/pdf')
        tests = b'"Input","OUtput","Categoria"\n"2020","Si\\n","Ano multiplo de 4"'
        tests = InMemoryUploadedFile(BytesIO(tests), 'tests', 'tests.csv', 'application/csv', len(tests), None, None)
        form_data = {
            'titulo':titulo,
            'statement':statement,
            'tests':tests
        }
        response = self.client.post(reverse('problemas:crear-problema', kwargs={'clase_id': self.clase_basica_1.id}), data = form_data, follow = True)
        assert len(Problema.objects.all()) == 0
        self.assertContains(response, 'El segundo Header debería ser Output, pero es OUtput')

    def test_incorrect_header_Categoria(self):
        self.client.force_login(user=self.usuaria_profesora)
        titulo = 'ProblemaTEST'
        statement = SimpleUploadedFile('statement.pdf', b'a', 'application/pdf')
        tests = b'"Input","Output","CAtegoria"\n"2020","Si\\n","Ano multiplo de 4"'
        tests = InMemoryUploadedFile(BytesIO(tests), 'tests', 'tests.csv', 'application/csv', len(tests), None, None)
        form_data = {
            'titulo':titulo,
            'statement':statement,
            'tests':tests
        }
        response = self.client.post(reverse('problemas:crear-problema', kwargs={'clase_id': self.clase_basica_1.id}), data = form_data, follow = True)
        assert len(Problema.objects.all()) == 0
        self.assertContains(response, 'El tercer Header debería ser Categoria, pero es CAtegoria')

    ''' 
    Al parecer el formato csv es mas robusto y no logre hacerlo fallar
    def test_invalid_csv(self):
        self.client.force_login(user=self.usuaria_profesora)
        titulo = 'ProblemaTEST'
        statement = SimpleUploadedFile('statement.pdf', b'a', 'application/pdf')
        tests = b''
        tests = InMemoryUploadedFile(BytesIO(tests), 'tests', 'tests.csv', 'application/csv', len(tests), None, None)
        form_data = {
            'titulo':titulo,
            'statement':statement,
            'tests':tests
        }
        response = self.client.post(reverse('problemas:crear-problema', kwargs={'clase_id': self.clase_basica_1.id}), data = form_data, follow = True)
        assert len(Problema.objects.all()) == 0
        self.assertContains(response, 'El archivo de test no es')
    '''
