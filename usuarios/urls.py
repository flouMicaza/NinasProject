from django.urls import path, include

from usuarios import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('auth/', include('django.contrib.auth.urls')),
]