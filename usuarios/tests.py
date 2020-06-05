from django.contrib import auth
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

# Create your tests here.
from cursos.models import Curso
from usuarios.models import User
from usuarios.views import IndexView


class InitialData(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuaria_prof = User.objects.create_user(username="profesora", password="contraseña123", es_profesora=True)

        self.usuaria_alumna = User.objects.create_user(username="alumna", password="contraseña123", es_alumna=True)

        self.usuaria_voluntaria = User.objects.create_user(username="voluntaria", password="contraseña123",
                                                           es_voluntaria=True)

        self.usuaria_coordinadora = User.objects.create_user(username="coordinadora", password="contraseña123",
                                                             es_coordinadora=True,
                                                             es_profesora=True)
        self.curso_basico = Curso.objects.create(nombre="C++: Básico")
        self.curso_basico.alumnas.add(self.usuaria_alumna)
        self.curso_basico.profesoras.add(self.usuaria_prof)
        self.curso_basico.voluntarias.add(self.usuaria_prof)


class LoginTest(InitialData):
    def setUp(self):
        super(LoginTest, self).setUp()

    def test_index_sin_login(self):
        response = self.client.get(reverse('usuarios:index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('usuarios:login'))

    def test_get_login(self):
        response = self.client.get(reverse('usuarios:login'))
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, 'Iniciar Sesión')

    def test_post_login(self):
        response = self.client.post(reverse('usuarios:login'), {'username': 'profesora', 'password': 'contraseña123'})
        self.assertTemplateNotUsed('registration/login.html')
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('usuarios:index'), status_code=302, target_status_code=302)

    def test_post_login_error(self):
        response = self.client.post(reverse('usuarios:login'), {'username': 'Flore', 'password': 'contraseña123'})
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, 'Usuario o contraseña incorrectos')

    '''def test_user_login(self):
        user = User.objects.get(username='Alumna')
        self.assertTrue(user.is_anonymous)
        response = self.client.post(reverse('usuarios:login'), {'username': 'Alumna', 'password': 'contraseña123'})
        user = User.objects.get(username='Alumna')
        self.assertFalse(user.is_anonymous)'''


class LogoutTest(InitialData):
    def setUp(self):
        super(LogoutTest, self).setUp()
        self.client.login(user=self.usuaria_prof)

    def test_get_logout(self):
        response = self.client.get(reverse('usuarios:logout'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('usuarios:index'), status_code=302, target_status_code=302)


class UserModelTest(InitialData):
    def setUp(self):
        super(UserModelTest, self).setUp()

    def test_user_is_profesora(self):
        usuaria_profesora = User.objects.get(username="profesora")
        self.assertEquals(self.usuaria_prof, usuaria_profesora)
        self.assertTrue(usuaria_profesora.es_profesora)
        self.assertFalse(usuaria_profesora.es_voluntaria)
        self.assertFalse(usuaria_profesora.es_coordinadora)
        self.assertFalse(usuaria_profesora.es_alumna)

    def test_user_is_voluntaria(self):
        usuaria_voluntaria = User.objects.get(username="voluntaria")
        self.assertEquals(self.usuaria_voluntaria, usuaria_voluntaria)
        self.assertFalse(usuaria_voluntaria.es_profesora)
        self.assertTrue(usuaria_voluntaria.es_voluntaria)
        self.assertFalse(usuaria_voluntaria.es_coordinadora)
        self.assertFalse(usuaria_voluntaria.es_alumna)


class IndexTest(InitialData):

    def setUp(self):
        super(IndexTest, self).setUp()

    def test_carga_inicio_profesora(self):
        self.client.force_login(user=self.usuaria_prof)
        response = self.client.get(reverse('usuarios:index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cursos:mis_cursos'))

    def test_carga_inicio_voluntaria(self):
        self.client.force_login(user=self.usuaria_voluntaria)
        response = self.client.get(reverse('usuarios:index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cursos:mis_cursos'))

    def test_carga_inicio_alumna(self):
        self.client.force_login(user=self.usuaria_alumna)
        curso_id = self.curso_basico.id
        response = self.client.get(reverse('usuarios:index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cursos:curso', kwargs={'curso_id': curso_id}))

    def test_get_curso_estudiante(self):
        curso_id = self.curso_basico.id
        index_view = IndexView()
        self.assertEquals(index_view.get_curso_estudiante(username=self.usuaria_alumna.username), curso_id)


class UserModelTest(InitialData):
    def setUp(self):
        super(UserModelTest, self).setUp()

    def test_menu_items_docente(self):
        menu_items = self.usuaria_prof.get_menu_items()
        self.menu_items = [("Mis cursos", '/'), ('Cambiar contraseña', '/reset-password/')]
        self.assertEquals(self.menu_items, menu_items)
        menu_items_voluntaria = self.usuaria_voluntaria.get_menu_items()
        self.assertEquals(self.menu_items, menu_items_voluntaria)

    def test_menu_items_coordinadora(self):
        #no habrá coordinadora por ahora.
        pass

    def test_menu_items_estudiante(self):
        pass


class MenuTest(InitialData):
    def setUp(self):
        super(MenuTest, self).setUp()

    def test_menu_docente(self):
        self.client.force_login(user=self.usuaria_prof)
        response = self.client.get(reverse('cursos:mis_cursos'))
        self.assertContains(response, 'Mis cursos')
        self.assertNotContains(response, 'Modo coordinadora')

    '''def test_menu_coordinadora(self):
        self.client.force_login(user=self.usuaria_coordinadora)
        response = self.client.get(reverse('cursos:mis_cursos'))
        self.assertContains(response, 'Mis cursos')
        self.assertContains(response, 'Modo coordinadora')
    '''