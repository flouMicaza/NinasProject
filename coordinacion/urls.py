from django.urls import path, include

from coordinacion import views

app_name = 'coordinadora'
urlpatterns = [
    path('inicio/', views.CoordinadoraInicioView.as_view(), name='inicio_coordinadora'),
    path('cursos', views.CoordinadoraCursosView.as_view(), name='cursos'),
    path('cursos/crear', views.CoordinadoraCrearCursosView.as_view(), name='crear_curso'),
    path('cursos/editar/<int:curso_id>', views.CoordinadoraEditarCursosView.as_view(), name='editar_curso'),
    path('cursos/eliminar/<int:curso_id>', views.eliminar_curso , name='eliminar_curso'),
    path('users', views.CoordinadoraUsersView.as_view(), name = 'users'),
    path('users/crear', views.CoordinadoraCrearUserView.as_view(), name = 'crear_user'),
    path('users/editar/<int:user_id>', views.CoordinadoraEditarUsersView.as_view(), name = 'editar_users'),
    path('users/eliminar/<int:user_id>', views.eliminar_user, name = 'eliminar_user')

]
