from usuarios.models import *
from cursos.models import *
curso_basico = Curso.objects.create(nombre="C++: Básico")
curso_avanzado = Curso.objects.create(nombre="C++: Avanzado")
curso_uandes = Curso.objects.create(nombre="Programación Uandes")



usuaria_profesora = User.objects.create_user(username="profesora", password="contraseña123",es_profesora=True)

usuaria_profesora2 = User.objects.create_user(username="profesora2", password="contraseña123",es_profesora=True)
usuaria_voluntaria = User.objects.create_user(username="voluntaria", password="contraseña123",es_voluntaria=True)

usuaria_voluntaria2 = User.objects.create_user(username="voluntaria2", password="contraseña123",es_voluntaria=True)

usuaria_voluntaria3 = User.objects.create_user(username="voluntaria3", password="contraseña123",es_voluntaria=True)

curso_basico.profesoras.add(usuaria_profesora2)
curso_basico.voluntarias.add(usuaria_voluntaria2)
curso_basico.voluntarias.add(usuaria_voluntaria3)


curso_avanzado.profesoras.add(usuaria_profesora2)
curso_avanzado.voluntarias.add(usuaria_voluntaria2)
curso_avanzado.voluntarias.add(usuaria_voluntaria3)


curso_uandes.profesoras.add(usuaria_profesora)
curso_uandes.voluntarias.add(usuaria_voluntaria)
