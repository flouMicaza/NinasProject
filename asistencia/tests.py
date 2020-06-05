import datetime
from datetime import date
from unittest.mock import Mock

from asistencia.models import Asistencia
from cursos.views import MisCursosView, CursosView
from usuarios.models import User
from django.urls import reverse
from django.test import TestCase, Client

from asistencia.utils import get_alumnas_en_orden, porcentaje_asistencia, clases_asistencias_alumna
from asistencia.views import *
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

        self.usuaria_alumna1 = User.objects.create_user(username="alumna1", first_name="Juana", last_name="Perez",
                                                        password="contraseña123", es_alumna=True)

        self.usuaria_alumna2 = User.objects.create_user(username="alumna2", first_name="Claudia", last_name="Muñoz",
                                                        password="contraseña123", es_alumna=True)

        self.usuaria_alumna3 = User.objects.create_user(username="alumna3", first_name="Claudia", last_name="Briones",
                                                        password="contraseña123", es_alumna=True)

        self.usuaria_alumna4 = User.objects.create_user(username="alumna4", first_name="Claudia", last_name="Opazo",
                                                        password="contraseña123", es_alumna=True)

        self.usuaria_alumna5 = User.objects.create_user(username="alumna5", first_name="Antonia", last_name="Quezada",
                                                        password="contraseña123", es_alumna=True)

        self.curso_basico = Curso.objects.create(nombre="C++: Básico", cant_clases=15)
        self.curso_basico.profesoras.add(self.usuaria_profesora1)
        self.curso_basico.voluntarias.add(self.usuaria_voluntaria1)
        self.curso_basico.voluntarias.add(self.usuaria_voluntaria2)
        self.curso_basico.alumnas.add(self.usuaria_alumna1)
        self.curso_basico.alumnas.add(self.usuaria_alumna2)
        self.curso_basico.alumnas.add(self.usuaria_alumna3)
        self.curso_basico.alumnas.add(self.usuaria_alumna4)
        self.curso_basico.alumnas.add(self.usuaria_alumna5)

        self.curso_avanzado = Curso.objects.create(nombre="C++: Avanzado", cant_clases=15)
        self.curso_avanzado.profesoras.add(self.usuaria_profesora2)
        self.curso_avanzado.voluntarias.add(self.usuaria_voluntaria2)
        self.curso_basico.alumnas.add(self.usuaria_alumna2)
        self.curso_basico.alumnas.add(self.usuaria_alumna3)
        self.curso_basico.alumnas.add(self.usuaria_alumna4)

        ## ASISTENCIA

        self.clase_basico1 = Clase.objects.create(nombre="Clase 1: Ciclos for", curso=self.curso_basico, fecha_clase=date(2020, 4, 4))
        self.clase_basico2 = Clase.objects.create(nombre="Clase 2: Ciclos while", curso=self.curso_basico, fecha_clase=date(2020, 4, 5))

        ## basico1 : alumna1, alumna3, alumna4, alumna2
        ## basico2 : alumna2, alumna4

        Asistencia.objects.create(alumna=self.usuaria_alumna1, clase=self.clase_basico1, 
                                  asistio=True)
        Asistencia.objects.create(alumna=self.usuaria_alumna2, clase=self.clase_basico1, 
                                  asistio=True)
        Asistencia.objects.create(alumna=self.usuaria_alumna3, clase=self.clase_basico1, 
                                  asistio=True)
        Asistencia.objects.create(alumna=self.usuaria_alumna4, clase=self.clase_basico1, 
                                  asistio=True)
        Asistencia.objects.create(alumna=self.usuaria_alumna5, clase=self.clase_basico1, 
                                  asistio=True)

        Asistencia.objects.create(alumna=self.usuaria_alumna1, clase=self.clase_basico2, 
                                  asistio=False)
        Asistencia.objects.create(alumna=self.usuaria_alumna2, clase=self.clase_basico2, 
                                  asistio=True)
        Asistencia.objects.create(alumna=self.usuaria_alumna3, clase=self.clase_basico2, 
                                  asistio=False)
        Asistencia.objects.create(alumna=self.usuaria_alumna4, clase=self.clase_basico2, 
                                  asistio=True)
        Asistencia.objects.create(alumna=self.usuaria_alumna5, clase=self.clase_basico2, 
                                  asistio=False)


class UtilsTest(InitialData):

    def setUp(self):
        super(UtilsTest, self).setUp()
        self.mi_curso = self.curso_basico
        self.alumnas_curso = self.mi_curso.alumnas.all()
        self.usuaria = self.mi_curso.alumnas.all()[0]

    def test_get_asistencias(self):
        lista_alumnas = list(self.alumnas_curso)
        alumnas_en_orden = get_alumnas_en_orden(self.alumnas_curso)

        self.assertEqual(len(alumnas_en_orden), len(self.alumnas_curso))

        for alumna in alumnas_en_orden:
            lista_alumnas.remove(alumna)

        # Revisa que esten todas las alumnas
        self.assertEqual(len(lista_alumnas), 0)

    '''def test_porcentaje_asistencia(self):
        nro_clases = len(Clase.objects.filter(curso=self.mi_curso))
        nro_asistencias = len(Asistencia.objects.filter(clase__curso=self.mi_curso, alumna=self.usuaria, asistio=True))
        porcentaje = int((nro_asistencias / nro_clases) * 100)
        porcentaje_calculado = porcentaje_asistencia(self.usuaria, self.mi_curso)
        self.assertEqual(porcentaje, porcentaje_calculado)
        self.assertTrue(porcentaje_calculado >= 0 and porcentaje_calculado <= 100)'''

    def test_asistencias_alumna(self):
        asistencias = Asistencia.objects.filter(alumna=self.usuaria, clase__curso=self.mi_curso).order_by('clase_id')
        clases_asistencias = clases_asistencias_alumna(self.usuaria, self.mi_curso)
        Clase.objects.create(nombre="mi_clase", curso=self.mi_curso,fecha_clase=date(2020, 4, 4))  # clase sin asistencias
        self.assertEqual(len(asistencias), len(clases_asistencias))
        self.assertNotEqual(len(clases_asistencias), len(Clase.objects.filter(curso=self.mi_curso)))

        for i in range(len(asistencias)):
            clase_asistencia = clases_asistencias[i]
            self.assertEqual(clase_asistencia[0], asistencias[i].clase)
            self.assertEqual(clase_asistencia[1], asistencias[i].asistio)


class Asistencia_GralViewTest(InitialData):

    def setUp(self):
        super(Asistencia_GralViewTest, self).setUp()
        self.asistencia_GralView = Asistencia_GralView()

    def test_get_asistencias(self):
        curso = self.curso_basico
        clases = Clase.objects.filter(curso=curso)
        alumnas_curso = list(curso.alumnas.all())
        asistencias = Asistencia.objects.filter(clase__curso=curso)

        lista_asistencias = self.asistencia_GralView.get_asistencias(asistencias, curso.alumnas.all())

        self.assertEqual(len(lista_asistencias), len(alumnas_curso))
        for lista in lista_asistencias:
            # Revisa que esten todas las clases
            self.assertEqual(len(lista[1]), len(clases))
            alumnas_curso.remove(lista[0])
        # Revisa que esten todas las alumnas
        self.assertEqual(len(alumnas_curso), 0)

        for asistencia in lista_asistencias:
            alumna = asistencia[0]
            # Revisa que el total de clases ṕor alumna sea correcto
            nro_clases = len(Asistencia.objects.filter(clase__in=clases, alumna=alumna, asistio=True))
            self.assertEqual(nro_clases, asistencia[2])

    def test_vista_gral_sin_alumnas(self):
        ## Acceder a la asistencia de un curso sin alumnas
        usuaria = self.usuaria_profesora1
        self.curso = Curso.objects.create(nombre="Django", cant_clases=15)
        self.curso.profesoras.add(usuaria)
        self.clase1 = Clase.objects.create(nombre="Clase 1: Modelos en Django", curso=self.curso,fecha_clase=date(2020, 4, 10))
        self.clase2 = Clase.objects.create(nombre="Clase 2: Administrador de Django", curso=self.curso,fecha_clase=date(2020, 5, 4))

        self.client.force_login(user=usuaria)

        response = self.client.get(reverse('asistencia:asistencia_gral', kwargs={'curso_id': self.curso.id}))
        self.assertTemplateUsed(response, 'asistencia/asistencia_gral.html')
        # Mensaje que arroja la página
        self.assertContains(response, "Este curso no tiene alumnas!")
        self.assertContains(response, "Volver")
        self.assertNotContains(response, "Alumna")
        self.assertNotContains(response, "Nombre")
        self.assertNotContains(response, "Total")

        self.client.logout()

    def test_vista_gral_sin_clases(self):
        ## Acceder a la asistencia de un curso sin clases
        usuaria = self.usuaria_profesora1
        self.curso = Curso.objects.create(nombre="Django", cant_clases=15)
        self.curso.profesoras.add(usuaria)
        self.curso.alumnas.add(self.usuaria_alumna1)
        self.curso.alumnas.add(self.usuaria_alumna2)

        self.client.force_login(user=usuaria)

        response = self.client.get(reverse('asistencia:asistencia_gral', kwargs={'curso_id': self.curso.id}))
        self.assertTemplateUsed(response, 'asistencia/asistencia_gral.html')
        # Mensaje que arroja la página
        self.assertContains(response, "Este curso no tiene clases!")
        self.assertContains(response, "Volver")
        self.assertNotContains(response, "Alumna")
        self.assertNotContains(response, "Nombre")
        self.assertNotContains(response, "Total")

        self.client.logout()

    def test_vista_gral_sin_clases_alumnas(self):
        ## Acceder a la asistencia de un curso sin clases
        usuaria = self.usuaria_profesora1
        self.curso = Curso.objects.create(nombre="Django", cant_clases=15)
        self.curso.profesoras.add(usuaria)

        self.client.force_login(user=usuaria)

        response = self.client.get(reverse('asistencia:asistencia_gral', kwargs={'curso_id': self.curso.id}))
        self.assertTemplateUsed(response, 'asistencia/asistencia_gral.html')
        # Mensaje que arroja la página
        self.assertContains(response, "Este curso no tiene clases ni alumnas!")
        self.assertContains(response, "Volver")
        self.assertNotContains(response, "Alumna")
        self.assertNotContains(response, "Nombre")
        self.assertNotContains(response, "Total")

        self.client.logout()

    def test_vista_gral_sin_asistencias(self):
        ## Acceder a la asistencia de un curso sin asistencias pasadas
        usuaria = self.usuaria_profesora1
        self.curso = Curso.objects.create(nombre="Django", cant_clases=15)
        self.curso.profesoras.add(usuaria)
        self.curso.alumnas.add(self.usuaria_alumna1)
        self.curso.alumnas.add(self.usuaria_alumna2)
        self.clase1 = Clase.objects.create(nombre="Clase 1: Modelos en Django", curso=self.curso,fecha_clase=date(2020, 5, 1))
        self.clase2 = Clase.objects.create(nombre="Clase 2: Administrador de Django", curso=self.curso,fecha_clase=date(2020, 10, 4))

        self.client.force_login(user=usuaria)

        response = self.client.get(reverse('asistencia:asistencia_gral', kwargs={'curso_id': self.curso.id}))
        self.assertTemplateUsed(response, 'asistencia/asistencia_gral.html')
        # Mensaje que arroja la página
        self.assertContains(response, "Aún no se ha pasado asistencia para este curso.")
        # self.assertContains(response, "PASAR ASISTENCIA")
        self.assertNotContains(response, "Alumna")
        self.assertNotContains(response, "Nombre")
        self.assertNotContains(response, "Total")

        self.client.logout()

    ## Modelo de test para la vista de las asistencia gral de un curso por una usuaria
    def vista_asistencia_gral(self, usuaria, curso):
        # Asistencias del curso
        asistencias = Asistencia.objects.filter(clase__curso=curso)

        # Las clases hechas hasta el momento
        clases = []
        for a in asistencias:
            if not a.clase in clases:
                clases += [a.clase]

        self.client.force_login(user=usuaria)
        response = self.client.get(reverse('asistencia:asistencia_gral', kwargs={'curso_id': curso.id}))
        self.assertTemplateUsed(response, 'asistencia/asistencia_gral.html')

        # self.assertContains(response, "PASAR ASISTENCIA")
        self.assertContains(response, "Asistencia")

        for clase in clases:
            self.assertContains(response, "Clase " + str(clase.id))
            nro_asistencias = len(Asistencia.objects.filter(clase=clase, asistio=True))
            self.assertContains(response, nro_asistencias)

        self.assertContains(response, "Alumna")
        self.assertContains(response, "Alumnas por clase")
        self.assertContains(response, "Clases Asistidas")

        for alumna in curso.alumnas.all():
            total_alumna = len(asistencias.filter(alumna=alumna, asistio=True))
            self.assertContains(response, total_alumna)
            self.assertContains(response, alumna.first_name)
            self.assertContains(response, alumna.last_name)

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
        ## Usuaria intenta ingresar a asistencia de curso al que no pertenece
        self.usuaria_profesora = User.objects.create_user(username="profesora", first_name="profesora",
                                                          password="contraseña123", es_profesora=True)
        self.client.force_login(user=self.usuaria_profesora)
        response = self.client.get(reverse('asistencia:asistencia_gral', kwargs={'curso_id': 1}))
        # self.assertTemplateUsed(response, 'error/403.html')
        self.assertEquals(response.status_code, 403)
        self.client.logout()


class MiCursoViewAlumnaTest(InitialData):

    def test_Mi_Curso_Alumna(self):
        curso = self.curso_basico
        usuaria = list(self.curso_basico.alumnas.all())[0]

        self.client.force_login(user=usuaria)

        response = self.client.get(reverse('cursos:curso', kwargs={'curso_id': curso.id}))
        self.assertTemplateUsed(response, 'cursos/inicio_curso.html')
        self.assertContains(response, curso.nombre)
        self.assertContains(response, 'Asistencia')
        self.assertContains(response, 'Ver Detalle')
        self.assertContains(response, '%')
        self.assertNotContains(response, 'Mis cursos')


class AsistenciaViewTest(InitialData):

    def setUp(self):
        super(AsistenciaViewTest, self).setUp()
        self.dia_ninaspro = 6  # 6 de Julio 2020 es sabado
        self.mes = 7
        self.anio = 2020
        self.hora_inicio = 10  # taller parte a las 10

    ## Test para la vista de las asistencia de un curso por una usuaria
    def vista_asistencia(self, day, hour, usuaria, curso):
        import datetime
        # Se establece una fecha y una hora
        newNow = datetime.datetime(year=self.anio, month=self.mes, day=day, hour=hour)
        datetime = Mock()
        datetime.datetime.return_value = newNow
        # Se crea una clase sin asistencias un dia de ninasṕro
        clase = Clase.objects.create(nombre="Clase prueba", curso=curso, fecha_clase=newNow)

        self.client.force_login(user=usuaria)
        response = self.client.get(
            reverse('asistencia:asistencia', kwargs={'curso_id': curso.id, 'clase_id': clase.id}))
        #self.assertTemplateUsed(response, 'asistencia/asistencia.html')
        self.assertContains(response, clase.nombre)
        self.assertContains(response, "Guardar")
        self.assertContains(response, "Asistencia")

        for alumna in curso.alumnas.all():
            self.assertContains(response, alumna.first_name + " " + alumna.last_name)

        self.client.logout()

    '''def test_vista_asistencia_dia_ninaspro(self):
        # Una voluntaria va a ṕasar la lista un dia de ninaspro a una hora permitida
        day = self.dia_ninaspro
        hour = self.hora_inicio + 1
        usuaria = self.usuaria_voluntaria1
        curso = Curso.objects.create(nombre="Django", cant_clases=15)
        curso.voluntarias.add(usuaria)
        curso.save()
        Clase.objects.create(nombre="Tutorial DjangoGirls", curso=curso,
                             fecha_clase=datetime.datetime(year=self.anio, month=self.mes, day=day, hour=hour))
        self.vista_asistencia(day, hour, usuaria, curso)'''

    #Se borra el test porque no está mal escrito.
    '''def test_vista_asistencia_dia_no_ninaspro(self):
        # Una profesora va a modificar la lista un dia que no hay ninaspro
        day = self.dia_ninaspro 
        hour = self.hora_inicio
        usuaria = self.usuaria_profesora1
        curso = list(Curso.objects.filter(profesoras__in=[usuaria]))[0]
        self.vista_asistencia(day, hour, usuaria, curso)'''

    ## Test para la vista de las asistencia de un curso por una usuaria sin permiso
    def vista_asistencia_sin_permiso(self, day, hour, usuaria, curso):
        import datetime
        # Se establece una fecha y una hora
        newNow = datetime.datetime(year=self.anio, month=self.mes, day=day, hour=hour)
        datetime = Mock()
        datetime.datetime.return_value = newNow
        # Se crea una clase sin asistencias un dia de ninaspro
        fecha_clase = datetime.datetime(year=self.anio, month=self.mes, day=self.dia_ninaspro)
        clase = Clase.objects.create(nombre="Clase prueba", curso=curso, fecha_clase=fecha_clase)

        self.client.force_login(user=usuaria)
        response = self.client.get(
            reverse('asistencia:asistencia', kwargs={'curso_id': curso.id, 'clase_id': clase.id}))
        # self.assertTemplateUsed(response, 'error/403.html')
        self.assertEquals(response.status_code, 302)
        self.client.logout()

    def test_vista_asistencia_inconsistente(self):
        ## Se ingresa a una clase y un curso que no es están relacionados
        usuaria = self.usuaria_profesora1
        curso = self.curso_basico  # debe tener clases creadas

        day = self.dia_ninaspro
        hour = self.hora_inicio
        clase = Clase.objects.filter(curso=curso).first()
        curso1 = Curso.objects.create(nombre="Curso prueba", cant_clases=15)
        curso1.profesoras.add(usuaria)
        curso1.alumnas.add(self.usuaria_alumna1)
        curso1.alumnas.add(self.usuaria_alumna2)

        self.client.force_login(user=usuaria)
        response = self.client.get(
            reverse('asistencia:asistencia', kwargs={'curso_id': curso1.id, 'clase_id': clase.id}))
        # self.assertTemplateUsed(response, 'error/403.html')
        self.assertEquals(response.status_code, 404)
        self.client.logout()

    def test_vista_asistencia_sin_permiso_voluntaria(self):
        ## Una voluntaria va a ṕasar la lista un dia de ninaspro fuera de horario
        day = self.dia_ninaspro
        hour = self.hora_inicio - 1
        usuaria = self.usuaria_voluntaria1
        curso = list(Curso.objects.filter(voluntarias__in=[usuaria]))[0]
        self.vista_asistencia_sin_permiso(day, hour, usuaria, curso)

    def test_vista_asistencia_sin_permiso_profesora(self):
        ## una profesora va a ṕasar la lista un dia de ninaspro antes de la clase
        day = self.dia_ninaspro -1
        hour = self.hora_inicio - 1
        usuaria = self.usuaria_voluntaria1
        curso = list(Curso.objects.filter(voluntarias__in=[usuaria]))[0]
        self.vista_asistencia_sin_permiso(day, hour, usuaria, curso)

    def test_vista_asistencia_sin_permiso_alumna(self):
        ## una alumna quiere ṕasar la lista
        day = self.dia_ninaspro
        hour = self.hora_inicio + 1
        usuaria = self.usuaria_alumna1
        curso = list(Curso.objects.filter(alumnas__in=[usuaria]))[0]
        self.vista_asistencia_sin_permiso(day, hour, usuaria, curso)

    def test_vista_asistencia_curso_no_existe(self):
        # probar el link con un curso que no existe y que tire 404.
        self.client.force_login(user=self.usuaria_profesora1)
        response = self.client.get(reverse('cursos:curso', kwargs={'curso_id': 5}))
        # self.assertTemplateUsed(response, 'error/404.html')
        self.assertEquals(response.status_code, 404)
