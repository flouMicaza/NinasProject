from django.urls import path, include

from coordinacion import views

app_name = 'coordinadora'
urlpatterns = [
    path('inicio/', views.CoordinadoraInicioView.as_view(), name='inicio_coordinadora'),

]
