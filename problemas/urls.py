import cursos
from django.urls import path
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

from problemas import views

app_name = 'problemas'

urlpatterns = [
    path('<int:curso_id>/curso/<int:problema_id>/problema/<int:result>', views.ProblemasViews.as_view(), name='detalle-problema'),
    path('<int:clase_id>/agregar-problema', views.CrearProblemasViews.as_view(), name='crear-problema'),
] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
