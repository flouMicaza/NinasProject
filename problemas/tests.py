import datetime
import base64
from django.test import TestCase, Client, LiveServerTestCase
from django.core.files.uploadedfile import SimpleUploadedFile, InMemoryUploadedFile
from io import BytesIO

# Create your tests here.
from django.urls import reverse

from NiñasProject.utils import problema_en_curso
from clases.models import Clase
from cursos.models import Curso
from usuarios.models import User
from problemas.models import Problema

# Cuando se actualice modelo:
# from coordinacion.models import Sede

class InitialData(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuaria_profesora = User.objects.create_user(username="profesora", password="contraseña123",
                                                          es_profesora=True)
        self.usuaria_profesora2 = User.objects.create_user(username="profesora2", password="contraseña123",
                                                           es_profesora=True)

        self.curso_basico = Curso.objects.create(nombre="C++: Básico")
        self.curso_basico.profesoras.add(self.usuaria_profesora)
        self.clase_basica_1 = Clase.objects.create(nombre="Variables", curso=self.curso_basico, publica=True,
                                                   fecha_clase=datetime.date(2019, 10, 19))

        self.curso_avanzado = Curso.objects.create(nombre="C++: Avanzado")
        self.curso_avanzado.profesoras.add(self.usuaria_profesora2)
        self.clase_avanzada_1 = Clase.objects.create(nombre="Ciclos For", curso=self.curso_avanzado, publica=True,
                                                   fecha_clase=datetime.date(2019, 10, 30))



class SubirArchivosTestJSON(InitialData):
    # probar que al cargar un curso se ven sus clases asociadas.
    def setUp(self):
        super(SubirArchivosTestJSON, self).setUp()

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
        self.assertContains(response, "Anno multiplo de 4")


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
        self.assertContains(response, "Ano multiplo de 4")

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


class PermisosProblemaTest(InitialData):

    def setUp(self):
        super(PermisosProblemaTest, self).setUp()

        statement_1 = SimpleUploadedFile('statement_1.pdf', b'a', 'application/pdf')
        tests_1 = b'[{\n    "Input":"2020", \n    "Output": "Si\\n", \n    "Categoria": "Anno multiplo de 4"}]'
        tests_1 = InMemoryUploadedFile(BytesIO(tests_1), 'tests', 'tests_1.json', 'application/json', len(tests_1), None, None)

        statement_2 = SimpleUploadedFile('statement_2.pdf', b'a', 'application/pdf')
        tests_2 = b'[{\n    "Input":"2001", \n    "Output": "No\\n", \n    "Categoria": "Anno no es multiplo de 4 ni de 400"}]'
        tests_2 = InMemoryUploadedFile(BytesIO(tests_2), 'tests', 'tests_2.json', 'application/json', len(tests_2), None, None)

        self.problema_basico = Problema.objects.create(titulo="Problema Básico",
                                                       fecha_creacion=datetime.date(2019, 11, 20),
                                                       statement=statement_1, tests=tests_1, clase=self.clase_basica_1)

        self.problema_avanzado = Problema.objects.create(titulo="Problema Avanzado",
                                                         fecha_creacion=datetime.date(2019, 11, 10),
                                                         statement=statement_2, tests=tests_2, clase=self.clase_avanzada_1)

    def test_problema_en_curso(self):
        self.assertEquals(problema_en_curso(self.problema_basico.id, self.curso_basico.id), True)
        self.assertEquals(problema_en_curso(self.problema_basico.id, self.curso_avanzado.id), False)
        self.assertEquals(problema_en_curso(self.problema_avanzado.id, self.curso_avanzado.id), True)
        self.assertEquals(problema_en_curso(self.problema_avanzado.id, self.curso_basico.id), False)

    def test_enunciado_curso_sin_permiso(self):
        self.client.force_login(user=self.usuaria_profesora)
        response = self.client.get(reverse('problemas:enunciado-problema', kwargs={'curso_id': self.curso_avanzado.id,
                                                                                   'problema_id': self.problema_basico.id,
                                                                                   'result': 1}))
        self.assertEquals(response.status_code, 302)

    def test_edicion_curso_sin_permiso(self):
        self.client.force_login(user=self.usuaria_profesora)
        response = self.client.get(reverse('problemas:editar-problema', kwargs={'curso_id': self.curso_avanzado.id,
                                                                                   'problema_id': self.problema_basico.id}))
        self.assertEquals(response.status_code, 302)

    def test_enunciado_problema_sin_permiso(self):
        self.client.force_login(user=self.usuaria_profesora2)
        response = self.client.get(reverse('problemas:enunciado-problema', kwargs={'curso_id': self.curso_avanzado.id,
                                                                                   'problema_id': self.problema_basico.id,
                                                                                   'result': 1}))
        self.assertEquals(response.status_code, 302)

    def test_edicion_problema_sin_permiso(self):
        self.client.force_login(user=self.usuaria_profesora2)
        response = self.client.get(reverse('problemas:editar-problema', kwargs={'curso_id': self.curso_avanzado.id,
                                                                                'problema_id': self.problema_basico.id}))
        self.assertEquals(response.status_code, 302)

    def test_enunciado_problema_no_existe(self):
        self.client.force_login(user=self.usuaria_profesora2)
        response = self.client.get(reverse('problemas:enunciado-problema', kwargs={'curso_id': self.curso_avanzado.id,
                                                                                   'problema_id': 10,
                                                                                   'result': 1}))
        self.assertEquals(response.status_code, 404)

    def test_editar_problema_no_existe(self):
        self.client.force_login(user=self.usuaria_profesora2)
        response = self.client.get(reverse('problemas:editar-problema', kwargs={'curso_id': self.curso_avanzado.id,
                                                                                   'problema_id': 10}))
        self.assertEquals(response.status_code, 404)

    def test_enunciado_curso_no_existe(self):
        self.client.force_login(user=self.usuaria_profesora)
        response = self.client.get(reverse('problemas:enunciado-problema', kwargs={'curso_id': 10,
                                                                                   'problema_id': self.problema_basico.id,
                                                                                   'result': 1}))
        self.assertEquals(response.status_code, 404)

    def test_editar_curso_no_existe(self):
        self.client.force_login(user=self.usuaria_profesora)
        response = self.client.get(reverse('problemas:editar-problema', kwargs={'curso_id': 10,
                                                                                'problema_id': self.problema_basico.id}))
        self.assertEquals(response.status_code, 404)

