import datetime
import base64
from django.test import TestCase, Client, LiveServerTestCase
from django.core.files.uploadedfile import SimpleUploadedFile, InMemoryUploadedFile
from io import BytesIO

# Create your tests here.
from django.urls import reverse

from NiñasProject.utils import problema_en_curso
from cursos.models import Curso
from usuarios.models import User
from coordinacion.models import Sede 
# Cuando se actualice modelo:
# from coordinacion.models import Sede

class InitialData(TestCase):
    def setUp(self):
        self.client = Client()

        self.usuaria_profesora = User.objects.create_user(username="user_profesora", password="contraseña123",
                                                          es_profesora=True)
        self.usuaria_alumna = User.objects.create_user(first_name = 'AlumnaTest', username="user_alumna", password="contraseña123",
                                                           es_alumna=True)
        self.usuaria_voluntaria = User.objects.create_user(username="user_voluntaria", password="contraseña123",
                                                           es_voluntaria=True)
        self.usuaria_coordinadora = User.objects.create_user(username="coordinadora", password="contraseña123",
                                                            es_coordinadora=True)
        self.sede = Sede.objects.create(nombre="FCFM", coordinadora=self.usuaria_coordinadora)
        self.curso_basico = Curso.objects.create(nombre="C++: Básico", sede=self.sede)


class UsuariasTest(InitialData):
    # probar que al cargar un curso se ven sus clases asociadas.
    def setUp(self):
        super(UsuariasTest, self).setUp()
        self.client.force_login(user=self.usuaria_coordinadora)

    def test_crear_user(self):
        form_data = {'first_name':'Usuaria', 
                    'last_name':'Test', 
                    'username':'UsuariaTest', 
                    'es_alumna':True,
                    'es_profesora':False, 
                    'es_voluntaria':False}
        self.client.post(reverse('coordinacion:crear_user'), data = form_data)
        us = User.objects.get(username='UsuariaTest')
        assert us.es_alumna and not us.es_profesora and not us.es_voluntaria
        assert us in self.sede.alumnas.all()
        response = self.client.get(reverse('coordinacion:users'))
        self.assertContains(response, "UsuariaTest")
    
    def test_eliminar_user(self):
        form_data = {'first_name':'Usuaria', 
                    'last_name':'Test', 
                    'username':'UsuariaTest', 
                    'es_alumna':True,
                    'es_profesora':False, 
                    'es_voluntaria':False}
        self.client.post(reverse('coordinacion:crear_user'), data = form_data)
        us = User.objects.get(username='UsuariaTest')
        self.client.get(reverse('coordinacion:eliminar_user', kwargs={'user_id':us.id}))
        us = User.objects.get(username='UsuariaTest')
        assert not us.is_active
        response = self.client.get(reverse('coordinacion:users'))
        self.assertNotContains(response, "UsuariaTest")
    
    def test_editar_user(self):
        form_data = {'first_name':'Usuaria', 
            'last_name':'Test', 
            'username':'UsuariaTest', 
            'es_alumna':True,
            'es_profesora':False, 
            'es_voluntaria':False}
        self.client.post(reverse('coordinacion:crear_user'), data = form_data)
        us = User.objects.get(username='UsuariaTest')
        form_data = {'first_name':'Edit', 
            'last_name':'Usuaria', 
            'es_alumna':False,
            'es_profesora':True, 
            'es_voluntaria':True}
        self.client.post(reverse('coordinacion:editar_users', kwargs={'user_id':us.id}), data = form_data)
        us2 = User.objects.get(username='UsuariaTest')
        assert us.first_name!=us2.first_name 
        assert us.last_name!=us2.last_name 
        assert not us2.es_alumna and us2.es_profesora and us2.es_voluntaria
        assert us2 in self.sede.profesoras.all() and us2 in self.sede.voluntarias.all() and us2 not in self.sede.alumnas.all()

    
    def test_eliminar_varios_users(self):
        form_data1 = {'first_name':'Usuaria', 
            'last_name':'Test', 
            'username':'UsuariaTest1', 
            'es_alumna':True,
            'es_profesora':False, 
            'es_voluntaria':False}
        form_data2 = {'first_name':'Usuaria', 
            'last_name':'Test', 
            'username':'UsuariaTest2', 
            'es_alumna':True,
            'es_profesora':False, 
            'es_voluntaria':False}
        self.client.post(reverse('coordinacion:crear_user'), data = form_data1)
        self.client.post(reverse('coordinacion:crear_user'), data = form_data2)
        us1 = User.objects.get(username='UsuariaTest1')
        us2 = User.objects.get(username='UsuariaTest2')
        form_delete = {
            'user_delete' : [us1.id, us2.id]
        }
        self.client.post(reverse('coordinacion:eliminar_users'), data=form_delete)
        us1 = User.objects.get(id=us1.id)
        us2 = User.objects.get(id=us2.id)
        assert not us1.is_active and not us2.is_active
        response = self.client.get(reverse('coordinacion:users'))
        self.assertNotContains(response, 'UsuariaTest1')
        self.assertNotContains(response, 'UsuariaTest2')


class CursosTest(InitialData):

    def setUp(self):
        super(CursosTest, self).setUp()
        self.client.force_login(user=self.usuaria_coordinadora)

    def test_crear_curso_view(self):
        request = self.client.get(reverse('coordinacion:crear_curso'))
        self.assertNotContains(request, self.usuaria_profesora.username)
        self.assertNotContains(request, self.usuaria_alumna.username)
        self.assertNotContains(request, self.usuaria_voluntaria.username)

        self.sede.profesoras.add(self.usuaria_profesora)
        self.sede.voluntarias.add(self.usuaria_voluntaria)
        self.sede.alumnas.add(self.usuaria_alumna)
        self.usuaria_profesora2 = User.objects.create_user(username="profesora2", password="contraseña123",
                                                          es_profesora=True)

        request = self.client.get(reverse('coordinacion:crear_curso'))
        self.assertContains(request, self.usuaria_profesora.username)
        self.assertContains(request, self.usuaria_alumna.username)
        self.assertContains(request, self.usuaria_voluntaria.username)
        self.assertNotContains(request, self.usuaria_profesora2.username)


    def test_crear_curso_no_data(self):
        form_data = {
            'nombre' : 'CursoTest',
            'profesoras' : [],
            'alumnas' : [],
            'voluntarias' : [],
            'lista_alumnas' : ''
        }
        self.client.post(reverse('coordinacion:crear_curso'), data=form_data)
        Curso.objects.get(nombre=form_data['nombre'], sede=self.sede)
        response = self.client.get(reverse('coordinacion:cursos'))
        self.assertContains(response, form_data['nombre'])

    def test_crear_curso_data(self):
        form_data = {
            'nombre' : 'CursoTest',
            'profesoras' : [self.usuaria_profesora.id],
            'alumnas' : [self.usuaria_alumna.id],
            'voluntarias' : [self.usuaria_voluntaria.id],
            'lista_alumnas' : ''
        }
        self.client.post(reverse('coordinacion:crear_curso'), data=form_data)
        curso = Curso.objects.get(nombre=form_data['nombre'], sede=self.sede)
        response = self.client.get(reverse('coordinacion:cursos'))
        self.assertContains(response, form_data['nombre'])
        assert self.usuaria_profesora in curso.profesoras.all()
        assert self.usuaria_alumna in curso.alumnas.all()
        assert self.usuaria_voluntaria in curso.voluntarias.all()


    # Por defecto, si se sube archivo csv, se ignora la lista de alumnas del campo 'alumnas'
    def test_crear_curso_csv(self):
        lista_alumnas = b'nombre,apellido,email\nUsuaria,CSV,UsuariaCSV'
        lista_alumnas = InMemoryUploadedFile(BytesIO(lista_alumnas), 'lista_alumnas', 
                        'lista_alumnas.csv', 'application/csv', len(lista_alumnas), None, None)

        form_data = {
            'nombre' : 'CursoTest',
            'profesoras' : [],
            'alumnas' : [self.usuaria_alumna.id],
            'voluntarias' : [],
            'lista_alumnas' : lista_alumnas
        }

        self.client.post(reverse('coordinacion:crear_curso'), data=form_data)

        curso = Curso.objects.get(nombre=form_data['nombre'], sede=self.sede)
        user = self.sede.alumnas.get(username = 'UsuariaCSV')
        assert user in curso.alumnas.all()
        assert self.usuaria_alumna not in curso.alumnas.all()
    
    def test_crear_curso_csv_usuarios_existen(self):
        lista_alumnas = b'nombre,apellido,email\nUsuaria,CSV,user_alumna'
        lista_alumnas = InMemoryUploadedFile(BytesIO(lista_alumnas), 'lista_alumnas', 
                        'lista_alumnas.csv', 'application/csv', len(lista_alumnas), None, None)

        form_data = {
            'nombre' : 'CursoTest',
            'profesoras' : [],
            'alumnas' : [self.usuaria_alumna.id],
            'voluntarias' : [],
            'lista_alumnas' : lista_alumnas
        }

        self.client.post(reverse('coordinacion:crear_curso'), data=form_data)
        curso = Curso.objects.get(nombre=form_data['nombre'], sede=self.sede)
        user = self.sede.alumnas.get(username = 'user_alumna')
        assert user in curso.alumnas.all()        
        assert  User.objects.get(username = 'user_alumna').first_name != 'Usuaria' 


    def test_editar_curso(self):
        form_data = {
            'nombre' : 'CursoEdit',
            'profesoras' : [self.usuaria_profesora.id],
            'alumnas' : [self.usuaria_alumna.id],
            'voluntarias' : [self.usuaria_voluntaria.id],
            'lista_alumnas' : ''
        }

        self.client.post(reverse('coordinacion:crear_curso'), data=form_data)
        curso = Curso.objects.get(nombre='CursoEdit')

        assert self.usuaria_profesora in curso.profesoras.all()
        assert self.usuaria_voluntaria in curso.voluntarias.all()
        assert self.usuaria_alumna in curso.alumnas.all()

        form_data = {
            'nombre' : 'CursoEdit2',
            'profesoras' : [],
            'alumnas' : [],
            'voluntarias' : []
        }
        self.client.post(reverse('coordinacion:editar_curso', kwargs={'curso_id':curso.id}), data=form_data)

        curso_edit = Curso.objects.get(id = curso.id)
        assert self.usuaria_profesora not in curso_edit.profesoras.all()
        assert self.usuaria_voluntaria not in curso_edit.voluntarias.all()
        assert self.usuaria_alumna not in curso_edit.alumnas.all()
        assert curso_edit.nombre == form_data['nombre']


    def test_eliminar_cursos(self):
        form_data1 = {
            'nombre' : 'CursoEdit',
            'profesoras' : [],
            'alumnas' : [],
            'voluntarias' : [],
            'lista_alumnas' : ''
        }

        form_data2 = {
            'nombre' : 'CursoEdit2',
            'profesoras' : [],
            'alumnas' : [],
            'voluntarias' : [],
            'lista_alumnas' : ''
        }

        self.client.post(reverse('coordinacion:crear_curso'), data = form_data1)
        self.client.post(reverse('coordinacion:crear_curso'), data = form_data2)
        curso1 = Curso.objects.get(nombre='CursoEdit')
        curso2 = Curso.objects.get(nombre='CursoEdit2')
        form_delete = {
            'cursos_delete' : [curso1.id, curso2.id]
        }
        self.client.post(reverse('coordinacion:eliminar_cursos'), data=form_delete)
        assert len(Curso.objects.filter(nombre='CursoEdit')) == 0
        assert len(Curso.objects.filter(nombre='CursoEdit2')) == 0

class AccesosTest(InitialData):
    def setUp(self):
        super(AccesosTest, self).setUp()

    def test_profesora(self):
        self.client.force_login(user=self.usuaria_profesora)
        response = self.client.get(reverse('coordinacion:inicio_coordinadora'))
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('coordinacion:cursos'))
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('coordinacion:crear_curso'))
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('coordinacion:editar_curso', kwargs={'curso_id': self.curso_basico.id}))
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('coordinacion:eliminar_curso', kwargs={'curso_id': self.curso_basico.id}))
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('coordinacion:eliminar_cursos'), data = {'users_eliminar':[]})
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('coordinacion:users'))
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('coordinacion:crear_user'))
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('coordinacion:editar_users', kwargs={'user_id': self.usuaria_alumna.id}))
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('coordinacion:eliminar_user', kwargs={'user_id': self.usuaria_alumna.id}))
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('coordinacion:eliminar_users'), data = {'users_eliminar':[]})
        self.assertEquals(response.status_code, 302)

    def test_alumna(self):
        self.client.force_login(user=self.usuaria_alumna)
        response = self.client.get(reverse('coordinacion:inicio_coordinadora'))
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('coordinacion:cursos'))
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('coordinacion:crear_curso'))
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('coordinacion:editar_curso', kwargs={'curso_id': self.curso_basico.id}))
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('coordinacion:eliminar_curso', kwargs={'curso_id': self.curso_basico.id}))
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('coordinacion:eliminar_cursos'), data = {'users_eliminar':[]})
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('coordinacion:users'))
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('coordinacion:crear_user'))
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('coordinacion:editar_users', kwargs={'user_id': self.usuaria_alumna.id}))
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('coordinacion:eliminar_user', kwargs={'user_id': self.usuaria_alumna.id}))
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('coordinacion:eliminar_users'), data = {'users_eliminar':[]})
        self.assertEquals(response.status_code, 302)

    def test_voluntaria(self):
        self.client.force_login(user=self.usuaria_voluntaria)
        response = self.client.get(reverse('coordinacion:inicio_coordinadora'))
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('coordinacion:cursos'))
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('coordinacion:crear_curso'))
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('coordinacion:editar_curso', kwargs={'curso_id': self.curso_basico.id}))
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('coordinacion:eliminar_curso', kwargs={'curso_id': self.curso_basico.id}))
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('coordinacion:eliminar_cursos'), data = {'users_eliminar':[]})
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('coordinacion:users'))
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('coordinacion:crear_user'))
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('coordinacion:editar_users', kwargs={'user_id': self.usuaria_alumna.id}))
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('coordinacion:eliminar_user', kwargs={'user_id': self.usuaria_alumna.id}))
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('coordinacion:eliminar_users'), data = {'users_eliminar':[]})
        self.assertEquals(response.status_code, 302)