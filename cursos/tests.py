from django.contrib.auth.models import User
from django.test import TestCase, Client

# Create your tests here.
from django.urls import reverse

from cursos.models import Curso
from usuarios.models import User


class CursosViewTest(TestCase):
    # probar que al cargar la pagina de una profesora o voluntaria muestre todos los curso que tiene asignados.
    # probar que al cargar la pagina de una alumna se muestre el curso al que pertenece.
    def setUp(self):
        self.client = Client()
        self.usuaria_profesora = User.objects.create_user(username="profesora", password="contraseña123",
                                                          es_profesora=True)
        self.client.force_login(user=self.usuaria_profesora)
        self.usuaria_profesora2 = User.objects.create_user(username="profesora2", password="contraseña123",
                                                           es_profesora=True)
        self.client.force_login(user=self.usuaria_profesora2)
        self.usuaria_voluntaria = User.objects.create_user(username="voluntaria", password="contraseña123",
                                                           es_voluntaria=True)
        self.client.force_login(user=self.usuaria_voluntaria)
        self.usuaria_voluntaria2 = User.objects.create_user(username="voluntaria2", password="contraseña123",
                                                            es_voluntaria=True)
        self.client.force_login(user=self.usuaria_voluntaria2)
        self.usuaria_voluntaria3 = User.objects.create_user(username="voluntaria3", password="contraseña123",
                                                            es_voluntaria=True)
        self.client.force_login(user=self.usuaria_voluntaria3)
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

    '''def test_profesora_tiene_cursos(self):
        response = self.client.get(reverse('usuarios:index'))
        self.assertContains(response, 'Programación Uandes')
        self.assertNotContains(response, 'C++: Avanzado')'''

    '''def test_voluntario_tiene_cursos(self):
        pass'''
