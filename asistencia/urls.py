from django.urls import path, include
from .views import get_form
from asistencia import views

app_name = 'asistencia'

urlpatterns = [
    path('<int:curso_id>/asistencia/', views.Asistencia_GralView.as_view(), name='asistencia_gral'),
    path('<int:curso_id>/asistencia/<int:clase_id>/', get_form, name='asistencia'),
]
