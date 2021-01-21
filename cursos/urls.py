from django.urls import path, include

from cursos import views

app_name = 'cursos'
urlpatterns = [
    path('<int:curso_id>/curso/', views.CursoView.as_view(), name='curso'),
    path('<int:curso_id>/curso/<str:order>/', views.CursoView.as_view(), name='curso'),
    path('mis_cursos/', views.MisCursosView.as_view(), name='mis_cursos'),
    path('<int:curso_id>/estadisticas/', views.EstadisticasView.as_view(), name='estadisticas'),

]
