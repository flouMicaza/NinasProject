from django.urls import path, include

from asistencia import views

app_name = 'asistencia'

urlpatterns = [
    path('<int:curso_id>/asistencia/', views.Asistencia_GralView.as_view(), name='asistencia_gral'),
    #path('<int:curso_id>/asistencia/clase_nombre', views.AsistenciaView.as_view(), name='asistencia'),
]
