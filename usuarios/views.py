from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, View):
    login_url = '/auth/login/'

    def get(self, request):
        return HttpResponse("Estoy logueado")



