from django.urls import path
from .views import get_form
from asistencia import views
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

app_name = 'asistencia'

urlpatterns = [
    path('<int:curso_id>/asistencia/', views.Asistencia_GralView.as_view(), name='asistencia_gral'),
    path('<int:curso_id>/asistencia/<int:clase_id>/', get_form, name='asistencia'),
] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
