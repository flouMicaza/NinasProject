from django.contrib import auth
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

# Create your tests here.
from usuarios.models import Cuenta


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuaria_prof = User(username="Florencia")
        self.usuaria_prof.save()
        self.usuaria_prof.password = "contraseña123"

        self.cuenta_usuaria = Cuenta(user=self.usuaria_prof, es_profesora=True)
        self.usuaria_alu = User(username="Alumna")
        self.usuaria_alu.save()
        self.usuaria_alu.password = "contraseña123"

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
        self.assertEquals(response.status_code, 200)
        #self.assertRedirects(response, reverse('usuarios:index'))

    def test_post_login_error(self):
        response = self.client.post(reverse('usuarios:login'), {'username': 'Flore', 'password': 'contraseña123'})
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, 'Usuario o contraseña incorrectos')

    '''def test_user_login(self):
        user = User.objects.get(username='Alumna')
        self.assertFalse(user.is_authenticated)
        response = self.client.post(reverse('usuarios:login'), {'username': 'Alumna', 'password': 'contraseña123'})
        self.assertTrue(user.is_authenticated)
    '''