import datetime

from django.test import TestCase, Client, LiveServerTestCase

# Create your tests here.
from django.urls import reverse

from clases.models import Clase
from cursos.models import Curso
from usuarios.models import User

'''
Clase para hacer mock de la fecha actual. 
'''


class InitialData(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuaria_profesora = User.objects.create_user(username="profesora", password="contraseña123",
                                                          es_profesora=True)

        self.usuaria_voluntaria = User.objects.create_user(username="voluntaria", password="contraseña123",
                                                           es_voluntaria=True)
        self.usuaria_voluntaria2 = User.objects.create_user(username="voluntaria2", password="contraseña123",
                                                            es_voluntaria=True)
        self.usuaria_alumna = User.objects.create_user(username="alumna", password="contraseña123",
                                                       es_alumna=True)

        self.curso_basico = Curso.objects.create(nombre="C++: Básico")
        self.curso_basico.profesoras.add(self.usuaria_profesora)
        self.curso_basico.voluntarias.add(self.usuaria_voluntaria)
        self.curso_basico.voluntarias.add(self.usuaria_voluntaria2)
        self.curso_basico.alumnas.add(self.usuaria_alumna)

        self.curso_avanzado = Curso.objects.create(nombre="C++: Avanzado")
        self.curso_avanzado.profesoras.add(self.usuaria_profesora)
        self.curso_avanzado.voluntarias.add(self.usuaria_voluntaria)
        self.curso_avanzado.voluntarias.add(self.usuaria_voluntaria2)

        self.curso_sin_clase = Curso.objects.create(nombre="Sin Clases")
        self.curso_sin_clase.voluntarias.add(self.usuaria_voluntaria)
        self.clase_basica_1 = Clase.objects.create(nombre="Variables", curso=self.curso_basico, publica=True,
                                                   fecha_clase=datetime.date(2019, 10, 19))
        self.clase_basica_2 = Clase.objects.create(nombre="Condiciones", curso=self.curso_basico, publica=False,
                                                   fecha_clase=datetime.date(2019, 10, 26))
        self.clase_avanzada_1 = Clase.objects.create(nombre="Matrices", curso=self.curso_avanzado, publica=True,
                                                     fecha_clase=datetime.date(2019, 11, 2))


class ClasesEnCursoTest(InitialData):
    # probar que al cargar un curso se ven sus clases asociadas.
    def setUp(self):
        super(ClasesEnCursoTest, self).setUp()


    def test_profesora_ve_clases(self):
        self.client.force_login(user=self.usuaria_profesora)
        response = self.client.get(reverse('cursos:curso', kwargs={'curso_id': self.curso_basico.id}))
        self.assertContains(response, "Variables")
        self.assertContains(response, "Condiciones")

    def test_alumna_ve_clases_publicas(self):
        self.client.force_login(user=self.usuaria_alumna)
        response = self.client.get(reverse('cursos:curso', kwargs={'curso_id': self.curso_basico.id}))
        self.assertContains(response, self.clase_basica_1.nombre)

    def test_voluntaria_ve_clases_publicas(self):
        self.client.force_login(user=self.usuaria_voluntaria)
        response = self.client.get(reverse('cursos:curso', kwargs={'curso_id': self.curso_basico.id}))
        self.assertContains(response, self.clase_basica_1.nombre)

    def test_alumna_no_ve_clases_privadas(self):
        self.client.force_login(user=self.usuaria_alumna)
        response = self.client.get(reverse('cursos:curso', kwargs={'curso_id': self.curso_basico.id}))
        self.assertNotContains(response, self.clase_basica_2.nombre)

    def test_profesora_puede_editar_clase(self):
        self.client.force_login(user=self.usuaria_profesora)
        response = self.client.get(reverse('cursos:curso', kwargs={'curso_id': self.curso_basico.id}))
        self.assertContains(response, 'create')

    def test_voluntaria_no_puede_editar(self):
        self.client.force_login(user=self.usuaria_voluntaria)
        response = self.client.get(reverse('cursos:curso', kwargs={'curso_id': self.curso_basico.id}))
        self.assertNotContains(response, 'create')

    def test_alumna_no_puede_editar(self):
        self.client.force_login(user=self.usuaria_alumna)
        response = self.client.get(reverse('cursos:curso', kwargs={'curso_id': self.curso_basico.id}))
        self.assertNotContains(response, 'create')

    def test_curso_sin_clases(self):
        self.client.force_login(user=self.usuaria_voluntaria)
        response = self.client.get(reverse('cursos:curso', kwargs={'curso_id': self.curso_sin_clase.id}))
        self.assertContains(response,"No hay clases disponibles para este curso.")
        response = self.client.get(reverse('cursos:curso', kwargs={'curso_id': self.curso_avanzado.id}))
        self.assertNotContains(response, "No hay clases disponibles para este curso.")

