from unittest.mock import Mock

from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase, Client

from asistencia.views import AsistenciaView
from clases.models import Clase
from cursos.models import Curso


class InitialData(TestCase):

    def setUp(self):
        ## USUARIOS

        self.client = Client()
        self.usuaria_profesora1 = User.objects.create_user(username="profesora1", first_name="profesora1",
                                                           password="contraseña123", es_profesora=True)

        self.usuaria_profesora2 = User.objects.create_user(username="profesora2", first_name="profesora2",
                                                           password="contraseña123", es_profesora=True)

        self.usuaria_voluntaria1 = User.objects.create_user(username="voluntaria", first_name="voluntaria",
                                                            password="contraseña123", es_voluntaria=True)

        self.usuaria_voluntaria2 = User.objects.create_user(username="voluntaria2", first_name="voluntaria2",
                                                            password="contraseña123", es_voluntaria=True)

        self.usuaria_alumna1 = User.objects.create_user(username="alumna1", first_name="alumna1",
                                                        password="contraseña123", es_alumna=True)

        self.usuaria_alumna2 = User.objects.create_user(username="alumna2", first_name="alumna2",
                                                        password="contraseña123", es_alumna=True)

        self.usuaria_alumna3 = User.objects.create_user(username="alumna3", first_name="alumna3",
                                                        password="contraseña123", es_alumna=True)

        self.usuaria_alumna4 = User.objects.create_user(username="alumna4", first_name="alumna4",
                                                        password="contraseña123", es_alumna=True)

        self.curso_basico = Curso.objects.create(nombre="C++: Básico")
        self.curso_basico.profesoras.add(self.usuaria_profesora1)
        self.curso_basico.voluntarias.add(self.usuaria_voluntaria1)
        self.curso_basico.voluntarias.add(self.usuaria_voluntaria2)
        self.curso_basico.alumnas.add(self.usuaria_alumna1)
        self.curso_basico.alumnas.add(self.usuaria_alumna2)
        self.curso_basico.alumnas.add(self.usuaria_alumna3)
        self.curso_basico.alumnas.add(self.usuaria_alumna4)

        self.curso_avanzado = Curso.objects.create(nombre="C++: Avanzado")
        self.curso_avanzado.profesoras.add(self.usuaria_profesora2)
        self.curso_avanzado.voluntarias.add(self.usuaria_voluntaria2)
        self.curso_basico.alumnas.add(self.usuaria_alumna2)
        self.curso_basico.alumnas.add(self.usuaria_alumna3)
        self.curso_basico.alumnas.add(self.usuaria_alumna4)

        ## ASISTENCIA

        self.clase_basico1 = Clase.objects.create(nombre="Clase 1: Ciclos for", curso=self.curso_basico)
        self.clase_basico2 = Clase.objects.create(nombre="Clase 2: Ciclos while", curso=self.curso_basico)


        for alumna in [self.usuaria_alumna1, self.usuaria_alumna2, self.usuaria_alumna3, self.usuaria_alumna4]:
            self.asistencia_basico1 = User.object.Asistencia(alumna=alumna, clase=self.clase_basico1,
                                                             curso=self.curso_basico)
            self.asistencia_basico2 = User.object.Asistencia(alumna=alumna, clase=self.clase_basico2,
                                                             curso=self.curso_basico)


class Asistencia_GralView(object):
    pass


class Asistencia_GralViewTest(InitialData):

    def setup(self):
        super(Asistencia_GralViewTest, self).setUp()
        self.asistencia_GralView = Asistencia_GralView()
        self.lista_cursos = self.misCursosView.get_cursos(self.usuaria_profesora2)


    def test_vista_asistenciaG_profesora(self):
        usuaria = self.usuaria_profesora1
        self.client.force_login(user=usuaria)
        curso = list(Curso.objects.filter(profesoras__in=[usuaria]))[0]
        response = self.client.get(reverse('asistencia:asistencia_gral', kwargs={'curso_id': curso.id}))
        self.assertTemplateUsed(response, 'asistencia:asistencia_gral.html')
        self.assertContains(response, "Pasar Asistencia")

        self.assertContains(response, "Asistencia")
        for clase in list(Clase.objects.filter(curso__in=[curso])):
            self.assertContains(response, clase.nombre)

        self.assertContains(response, "Nombre")
        self.assertContains(response, "Total")

        for alumna in curso.alumnas:
            self.assertContains(response, alumna.name)

        self.client.logout()


    def test_vista_asistenciaG_voluntaria(self):
        usuaria = self.usuaria_voluntaria2
        self.client.force_login(user=usuaria)
        curso = list(Curso.objects.filter(profesoras__in=[usuaria]))[0]
        response = self.client.get(reverse('asistencia:asistencia_gral', kwargs={'curso_id': curso.id}))
        self.assertTemplateUsed(response, 'asistencia:asistencia_gral.html')
        self.assertContains(response, "Pasar Asistencia")

        self.assertContains(response, "Asistencia")
        for clase in list(Clase.objects.filter(curso__in=[curso])):
            self.assertContains(response, clase.nombre)

        self.assertContains(response, "Nombre")
        self.assertContains(response, "Total")

        for alumna in curso.alumnas:
            self.assertContains(response, alumna.name)

        self.client.logout()


    def test_curso_sin_permiso(self):
        self.usuaria_profesora = User.objects.create_user(username="profesora", first_name="profesora",
                                                           password="contraseña123", es_profesora=True)

        self.client.force_login(user=self.usuaria_profesora)
        curso_id = self.lista_cursos[0].id
        response = self.client.get(reverse('asistencia:asistencia_gral', kwargs={'curso_id': curso_id}))
        # self.assertTemplateUsed(response, 'error/403.html')
        self.assertEquals(response.status_code, 403)


class AsistenciaViewTest(InitialData):

    def setUp(self):
        super(AsistenciaViewTest, self).setUp()
        self.asistenciaView = AsistenciaView()
        self.lista_cursos = self.misCursosView.get_cursos(self.usuaria_profesora2)


    def test_vista_asistencia_sabado(self):
        import datetime
        ## una voluntaria va a ṕasar la lista un sabado a las 11:30
        
        self.client.force_login(user=self.usuaria_voluntaria1)
        newNow = datetime.datetime(year=2020, month=6, day=6, hour= 11, minute=30) #sabado
        datetime = Mock()
        datetime.datetime.return_value = newNow

        curso_id = self.lista_cursos[0].id
        response = self.client.get(reverse('asistencia:asistencia', kwargs={'curso_id': curso_id}))
        self.assertTemplateUsed(response, 'asistencia:asistencia_gral.html')
        self.assertContains(response, "Save")

        self.assertContains(response, "Asistencia")
        self.assertContains(response, "Clase 1")
        self.assertContains(response, "Clase 2")
        self.assertContains(response, "Nombre")

        for i in range(4):
            self.assertContains(response, "alumna" + str(i+1))

        self.client.logout()


    def test_vista_asistencia_domingo(self):
        import datetime
        ## una profesora va a modificar la lista un domingo

        self.client.force_login(user=self.usuaria_profesora1)
        newNow = datetime.datetime(year=2020, month=6, day=6, hour=11, minute=30)
        datetime = Mock()
        datetime.datetime.return_value = newNow

        curso_id = self.lista_cursos[0].id
        response = self.client.get(reverse('asistencia:asistencia', kwargs={'curso_id': curso_id}))
        self.assertTemplateUsed(response, 'asistencia:asistencia_gral.html')
        self.assertContains(response, "Save")

        self.assertContains(response, "Asistencia")
        self.assertContains(response, "Clase 1")
        self.assertContains(response, "Clase 2")
        self.assertContains(response, "Nombre")

        for i in range(4):
            self.assertContains(response, "alumna" + str(i + 1))

        self.client.logout()


    def test_vista_asistencia_sin_permiso_sabado(self):
        import datetime
        ## una voluntaria va a ṕasar la lista un sabado a las 7 am

        self.client.force_login(user=self.usuaria_voluntaria1)
        newNow = datetime.datetime(year=2020, month=6, day=7, hour=7)
        datetime = Mock()
        datetime.datetime.return_value = newNow

        curso_id = self.lista_cursos[0].id
        response = self.client.get(reverse('asistencia:asistencia', kwargs={'curso_id': curso_id}))
        self.assertTemplateUsed(response, 'asistencia:asistencia_gral.html')
        self.assertContains(response, "Save")

        self.assertContains(response, "Asistencia")
        self.assertContains(response, "Clase 1")
        self.assertContains(response, "Clase 2")
        self.assertContains(response, "Nombre")

        for i in range(4):
            self.assertContains(response, "alumna" + str(i + 1))

        self.client.logout()


    def test_vista_asistencia_sin_permiso(self):
        ## una alumna quiere ṕasar la lista

        self.client.force_login(user=self.usuaria_alumna3)

        curso_id = self.lista_cursos[0].id
        response = self.client.get(reverse('asistencia:asistencia', kwargs={'curso_id': curso_id}))
        self.assertTemplateUsed(response, 'asistencia:asistencia_gral.html')
        self.assertContains(response, "Save")

        self.assertContains(response, "Asistencia")
        self.assertContains(response, "Clase 1")
        self.assertContains(response, "Clase 2")
        self.assertContains(response, "Nombre")

        for i in range(4):
            self.assertContains(response, "alumna" + str(i + 1))

        self.client.logout()







