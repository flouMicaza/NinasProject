from django.contrib import auth
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

# Create your tests here.
from usuarios.models import User


class LoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuaria_prof = User.objects.create(username="Florencia", password="contraseña123",es_profesora=True)

        self.usuaria_alu = User.objects.create(username="Alumna",password="contraseña123",es_alumna=True)

    def test_index_sin_login(self):
        response = self.client.get(reverse('usuarios:index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('usuarios:login'))

    def test_get_login(self):
        response = self.client.get(reverse('usuarios:login'))
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, 'Iniciar Sesión')

    def test_post_login(self):
        response = self.client.post(reverse('usuarios:login'), {'username': 'Florencia', 'password': 'contraseña123'})
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('usuarios:index'))

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


class LogoutTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuaria_prof = User.objects.create_user(username="Florencia", password="contraseña123")
        self.cuenta_usuaria = User.objects.create(user=self.usuaria_prof, es_profesora=True)

        self.client.login(user=self.usuaria_prof)

    def test_get_logout(self):
        response = self.client.get(reverse('usuarios:logout'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('usuarios:index'))
