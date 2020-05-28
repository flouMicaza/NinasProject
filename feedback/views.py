from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views import View

from feedback.models import OutputAlternativo
from problemas.models import Caso


class CasosAlternativos(LoginRequiredMixin, View):
    def post(self, request):
        if request.is_ajax():
            id_caso = request.POST.get('id')
            caso = Caso.objects.get(id=id_caso)
            outputs_sugeridos = OutputAlternativo.objects.filter(caso=caso, agregado=False,frecuencia__gt=1)
            outputs_agregados = OutputAlternativo.objects.filter(caso=caso, agregado=True)
            context = {
                'id_caso': id_caso,
                'caso': caso,
                'outputs_sugeridos': outputs_sugeridos,
                'outputs_agregados': outputs_agregados
            }
            return render(request, 'problemas/modal_casos_alternativos.html', context)

        else:
            return render(request, 'problemas/feedback_error.html', {'error': 'No se hizo una request ajax'})