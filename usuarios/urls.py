from django.urls import path, include

from usuarios import views

app_name = 'usuarios'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('reset-password/', views.ResetPassword.as_view(),name='reset-password')
]
