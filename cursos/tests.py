from django.contrib.auth.models import User
from django.test import TestCase, Client

# Create your tests here.
from django.urls import reverse

from usuarios.models import User


class CursosTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.usuaria_prof = User.objects.create_user(username="profesora", password="contraseña123", es_profesora=True)

        self.usuaria_alumna = User.objects.create_user(username="alumna", password="contraseña123", es_alumna=True)

        self.usuaria_voluntaria = User.objects.create_user(username="voluntaria", password="contraseña123",
                                                           es_voluntaria=True)

        self.usuaria_coordinadora = User.objects.create_user(username="coordinadora", password="contraseña123",
                                                             es_coordinadora=True,
                                                             es_profesora=True)

    def test_carga_inicio_profe(self):
        self.client.force_login(user=self.usuaria_prof)
        response = self.client.get(reverse('usuarios:index'))
        self.assertTemplateUsed(response, 'cursos/inicio_docente.html')
        self.assertContains(response, 'Mis cursos')

    def test_carga_inicio_voluntaria(self):
        self.client.force_login(user=self.usuaria_voluntaria)
        response = self.client.get(reverse('usuarios:index'))
        self.assertTemplateUsed(response, 'cursos/inicio_docente.html')
        self.assertContains(response, 'Mis cursos')

    def test_carga_inicio_alumna(self):
        self.client.force_login(user=self.usuaria_alumna)
        response = self.client.get(reverse('usuarios:index'))
        self.assertTemplateUsed(response, 'cursos/inicio_curso.html')
        self.assertContains(response, 'C++ Básico')
