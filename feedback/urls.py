from django.urls import path
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from feedback import views

app_name = 'feedback'
urlpatterns = [
    path('casos-alternativos', views.CasosAlternativos.as_view(),name='casos-alternativos'),
   ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)