import datetime
from datetime import date
from unittest.mock import Mock

from asistencia.models import Asistencia
from cursos.views import MisCursosView, CursosView
from usuarios.models import User
from django.urls import reverse
from django.test import TestCase, Client

from asistencia.views import Asistencia_GralView, AsistenciaView
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
            self.asistencia_basico1 = Asistencia.objects.create(alumna=alumna, clase=self.clase_basico1, author= self.usuaria_profesora1)
            self.asistencia_basico2 = Asistencia.objects.create(alumna=alumna, clase=self.clase_basico2, author= self.usuaria_profesora1)


class Asistencia_GralViewTest(InitialData):

    def setup(self):
        super(Asistencia_GralViewTest, self).setUp()
        self.asistencia_GralView = Asistencia_GralView()

    # Test para la vista de las asistencia gral de un curso por una usuaria
    def vista_asistencia_gral(self, usuaria, curso):
        self.client.force_login(user=usuaria)
        response = self.client.get(reverse('asistencia:asistencia_gral', kwargs={'curso_id': curso.id}))
        self.assertTemplateUsed(response, 'asistencia/asistencia_gral.html')
        self.assertContains(response, "Pasar Asistencia")

        self.assertContains(response, "Asistencia")
        for clase in list(Clase.objects.filter(curso__in=[curso])):
            self.assertContains(response, clase.nombre)

        self.assertContains(response, "Nombre")
        self.assertContains(response, "Total")

        for alumna in curso.alumnas:
            self.assertContains(response, alumna.name)

        self.client.logout()


    def test_vista_asistencia_gral_profesora(self):
        usuaria = self.usuaria_profesora1
        curso = list(Curso.objects.filter(profesoras__in=[usuaria]))[0]
        self.vista_asistencia_gral(usuaria, curso)


    def test_vista_asistencia_gral_voluntaria(self):
        usuaria = self.usuaria_voluntaria2
        curso = list(Curso.objects.filter(voluntarias__in=[usuaria]))[0]
        self.vista_asistencia_gral(usuaria, curso)


    def test_curso_sin_permiso(self):
        self.usuaria_profesora = User.objects.create_user(username="profesora", first_name="profesora",
                                                           password="contraseña123", es_profesora=True)
        self.client.force_login(user=self.usuaria_profesora)
        response = self.client.get(reverse('asistencia:asistencia_gral', kwargs={'curso_id': 1}))
        # self.assertTemplateUsed(response, 'error/403.html')
        self.assertEquals(response.status_code, 403)
        self.client.logout()


class AsistenciaViewTest(InitialData):

    def setUp(self):
        super(AsistenciaViewTest, self).setUp()
        self.asistenciaView = AsistenciaView()
        self.dia_ninaspro= 6 #6 de Julio 2020 es sabado
        self.hora_inicio = 10 #taller parte a las 10


    # Test para la vista de las asistencia un curso por una usuaria
    def vista_asistencia(self, day, hour, usuaria, curso):
        import datetime
        clase = list(Clase.objects.filter(curso=curso))[0]
        newNow = datetime.datetime(year=2020, month=6, day=day, hour=hour)
        datetime = Mock()
        datetime.datetime.return_value = newNow

        self.client.force_login(user=usuaria)
        response = self.client.get(reverse('asistencia:asistencia', kwargs={'curso_id': curso.id,'clase_id': clase.id}))
        self.assertTemplateUsed(response, 'asistencia/asistencia.html')
        self.assertContains(response, "Save")
        self.assertContains(response, "Asistencia")
        for clase in list(Clase.objects.filter(curso__in=[curso])):
            self.assertContains(response, clase.nombre)
        self.assertContains(response, "Nombre")
        for i in range(4):
            self.assertContains(response, "alumna" + str(i + 1))

        self.client.logout()


    def test_vista_asistencia_dia_ninaspro(self):
        ## una voluntaria va a ṕasar la lista un dia de ninaspro a una hora permitida
        day = self.dia_ninaspro
        hour = self.hora_inicio + 1
        usuaria = self.usuaria_voluntaria1
        curso = Curso.objects.create(nombre="Django")
        curso.voluntarias.add(usuaria)
        Clase.objects.create(nombre="Tutorial DjangoGirls", curso=curso, fecha_clase= datetime.datetime(year=2020, month=6, day=day, hour=hour))
        self.vista_asistencia(day, hour, usuaria, curso)


    def test_vista_asistencia_dia_no_ninaspro(self):
        ## una profesora va a modificar la lista un dia que no hay ninaspro
        day = self.dia_ninaspro+1
        hour = self.hora_inicio
        usuaria = self.usuaria_profesora1
        curso = list(Curso.objects.filter(profesoras__in=[usuaria]))[0]
        self.vista_asistencia(day, hour, usuaria, curso)


    # Test para la vista de las asistencia de un curso por una usuaria sin permiso
    def vista_asistencia_sin_permiso(self, day, hour, usuaria, curso):
        import datetime
        clase = list(Clase.objects.filter(curso=curso))[0]
        newNow = datetime.datetime(year=2020, month=6, day=day, hour=hour)
        datetime = Mock()
        datetime.datetime.return_value = newNow
        self.client.force_login(user=usuaria)
        response = self.client.get(reverse('asistencia:asistencia', kwargs={'curso_id': curso.id,'clase_id': clase.id}))
        # self.assertTemplateUsed(response, 'error/403.html')
        self.assertEquals(response.status_code, 403)
        self.client.logout()


    def test_vista_asistencia_sin_permiso_voluntaria(self):
        ## una voluntaria va a ṕasar la lista un dia de ninaspro fuera de horario
        day = self.dia_ninaspro
        hour = self.hora_inicio-1
        usuaria = self.usuaria_voluntaria1
        curso = list(Curso.objects.filter(voluntarias__in=[usuaria]))[0]
        self.vista_asistencia_sin_permiso(day, hour, usuaria, curso)


    def test_vista_asistencia_sin_permiso_profesora(self):
        ## una profesora va a ṕasar la lista un dia de ninaspro antes de la clase
        day = self.dia_ninaspro
        hour = self.hora_inicio-1
        usuaria = self.usuaria_voluntaria1
        curso = list(Curso.objects.filter(voluntarias__in=[usuaria]))[0]
        self.vista_asistencia_sin_permiso(day, hour, usuaria, curso)


    def test_vista_asistencia_sin_permiso_alumna(self):
        ## una alumna quiere ṕasar la lista
        day = self.dia_ninaspro
        hour = self.hora_inicio+1
        usuaria = self.usuaria_alumna1
        curso = list(Curso.objects.filter(alumnas__in=[usuaria]))[0]
        self.vista_asistencia_sin_permiso(day, hour, usuaria, curso)

    def test_vista_asistencia_curso_no_existe(self):
        # probar el link con un curso que no existe y que tire 404.
        self.client.force_login(user=self.usuaria_profesora1)
        response = self.client.get(reverse('cursos:curso', kwargs={'curso_id': 5}))
        # self.assertTemplateUsed(response, 'error/404.html')
        self.assertEquals(response.status_code, 404)






