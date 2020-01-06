from django.urls import path, include

from asistencia import views

app_name = 'asistencia'

urlpatterns = [
    path('<int:curso_id>/asistencia/', views.AsistenciaView.as_view(), name='asistencia'),
]
