from django.urls import path, include

from clases import views

app_name = 'clases'
urlpatterns = [
    path('<int:curso_id>/agregar-clase/', views.CrearClaseView.as_view(), name='agregar_clase'),
]