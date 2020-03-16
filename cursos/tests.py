from django.contrib.auth.models import User
from django.test import TestCase, Client, LiveServerTestCase, selenium

# Create your tests here.
from django.urls import reverse
#from selenium.webdriver.chrome.webdriver import WebDriver

from cursos.models import Curso
from cursos.views import MisCursosView
from usuarios.models import User
from usuarios.views import IndexView


class InitialData(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuaria_profesora = User.objects.create_user(username="profesora", password="contraseña123",
                                                          es_profesora=True)

        self.usuaria_profesora2 = User.objects.create_user(username="profesora2", password="contraseña123",
                                                           es_profesora=True)
        self.usuaria_voluntaria = User.objects.create_user(username="voluntaria", password="contraseña123",
                                                           es_voluntaria=True)
        self.usuaria_voluntaria2 = User.objects.create_user(username="voluntaria2", password="contraseña123",
                                                            es_voluntaria=True)
        self.usuaria_voluntaria3 = User.objects.create_user(username="voluntaria3", password="contraseña123",
                                                            es_voluntaria=True)
        self.curso_basico = Curso.objects.create(nombre="C++: Básico")
        self.curso_basico.profesoras.add(self.usuaria_profesora2)
        self.curso_basico.voluntarias.add(self.usuaria_voluntaria2)
        self.curso_basico.voluntarias.add(self.usuaria_voluntaria3)

        self.curso_avanzado = Curso.objects.create(nombre="C++: Avanzado")
        self.curso_avanzado.profesoras.add(self.usuaria_profesora2)
        self.curso_avanzado.voluntarias.add(self.usuaria_voluntaria2)
        self.curso_avanzado.voluntarias.add(self.usuaria_voluntaria3)

        self.curso_uandes = Curso.objects.create(nombre="Programación Uandes")
        self.curso_uandes.profesoras.add(self.usuaria_profesora)
        self.curso_uandes.voluntarias.add(self.usuaria_voluntaria)


class MisCursosViewTest(InitialData):
    # probar que al cargar mis cursos de una profesora o voluntaria muestre todos los curso que tiene asignados.

    def setUp(self):
        super(MisCursosViewTest, self).setUp()
        self.misCursosView = MisCursosView()

    def test_get_cursos_docente(self):
        lista_cursos = self.misCursosView.get_cursos(self.usuaria_profesora2)
        self.assertTrue(set([self.curso_basico, self.curso_avanzado]).issuperset(set(lista_cursos)))

    # Vista de inicio docente carga página mis cursos y muestra los respectivos cursos.
    def test_vista_inicio_profesora(self):
        self.client.force_login(user=self.usuaria_profesora2)
        response = self.client.get(reverse('cursos:mis_cursos'))
        self.assertTemplateUsed(response, 'cursos/mis_cursos.html')
        self.assertContains(response, "C++: Avanzado")
        self.assertContains(response, "C++: Básico")
        self.client.logout()

    # Vista de inicio docente carga página mis cursos y muestra los respectivos cursos.
    def test_vista_inicio_voluntaria(self):
        self.client.force_login(user=self.usuaria_voluntaria)
        response = self.client.get(reverse('cursos:mis_cursos'))
        self.assertTemplateUsed(response, 'cursos/mis_cursos.html')
        self.assertContains(response, "Programación Uandes")
        self.client.logout()


class CursoViewTest(InitialData,TestCase):
    def setUp(self):
        super(CursoViewTest, self).setUp()
        self.usuaria_estudiante = User.objects.create_user(username="estudiante", password="contraseña123",
                                                           es_alumna=True)
        self.curso_basico.alumnas.add(self.usuaria_estudiante)

        self.misCursosView = MisCursosView()
        self.index_view = IndexView()

    # Vista inicio estudiante carga pagina de un curso y muestra info de ese curso.

    def test_vista_inicio_estudiante(self):
        self.client.force_login(user=self.usuaria_estudiante)

        curso_id = self.index_view.get_id_curso_estudiante(username=self.usuaria_estudiante.username)
        response = self.client.get(reverse('cursos:curso', kwargs={'curso_id': curso_id}))
        self.assertTemplateUsed(response, 'cursos/inicio_curso.html')
        self.assertContains(response, 'C++: Básico')
        self.assertNotContains(response, 'Mis cursos')

    def test_curso_profesora(self):
        self.client.force_login(user=self.usuaria_profesora2)
        lista_cursos = self.misCursosView.get_cursos(self.usuaria_profesora2)
        primer_curso = lista_cursos[0]
        response = self.client.get(reverse('cursos:curso', kwargs={'curso_id': primer_curso.id}))
        self.assertTemplateUsed(response, 'cursos/inicio_curso.html')
        self.assertContains(response, primer_curso.nombre)
        self.assertNotContains(response, 'Mi curso')

    def test_curso_voluntaria(self):
        self.client.force_login(user=self.usuaria_voluntaria2)
        lista_cursos = self.misCursosView.get_cursos(self.usuaria_voluntaria2)
        primer_curso = lista_cursos[0]
        response = self.client.get(reverse('cursos:curso', kwargs={'curso_id': primer_curso.id}))
        self.assertTemplateUsed(response, 'cursos/inicio_curso.html')
        self.assertContains(response, primer_curso.nombre)
        self.assertNotContains(response, 'Mi curso')

    def test_curso_no_existe(self):
        # probar el link con un curso que no existe y que tire 404.
        self.client.force_login(user=self.usuaria_profesora2)
        response = self.client.get(reverse('cursos:curso', kwargs={'curso_id': 5}))
        # self.assertTemplateUsed(response, 'error/404.html')
        self.assertEquals(response.status_code, 404)

    def test_curso_sin_permiso(self):
        self.client.force_login(user=self.usuaria_profesora2)
        otro_curso = 3
        response = self.client.get(reverse('cursos:curso', kwargs={'curso_id': otro_curso}))
        # self.assertTemplateUsed(response, 'error/403.html')
        self.assertEquals(response.status_code, 403)


