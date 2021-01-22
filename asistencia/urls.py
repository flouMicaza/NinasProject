import cursos
from django.urls import path
from .views import get_form, clear_cache
from asistencia import views
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

app_name = 'asistencia'

urlpatterns = [
    path('<int:curso_id>/asistencia/', views.Asistencia_GralView.as_view(), name='asistencia_gral'),
    path('<int:curso_id>/asistencia/<int:clase_id>/', get_form, name='asistencia'),
    path('<int:curso_id>/asistencia/<int:clase_id>/cache', clear_cache, name="asistencia_cache")
] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
