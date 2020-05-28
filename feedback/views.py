from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View

from NiñasProject.decorators import  docente_required
from feedback.forms import OutputAlternativoModelFormSet
from feedback.models import OutputAlternativo
from problemas.models import Caso


@method_decorator([docente_required], name='dispatch')
class CasosAlternativos(LoginRequiredMixin, View):
    def get(self, request):
        if request.is_ajax():
            id_caso = request.GET.get('id')
            caso = Caso.objects.get(id=id_caso)
            outputs_sugeridos = OutputAlternativo.objects.filter(caso=caso, agregado=False, frecuencia__gt=1)
            outputs_agregados = OutputAlternativo.objects.filter(caso=caso, agregado=True)

            formset = OutputAlternativoModelFormSet(queryset=outputs_sugeridos)

            context = {
                'id_caso': id_caso,
                'caso': caso,
                'outputs_sugeridos': outputs_sugeridos,
                'outputs_agregados': outputs_agregados,
                'formset': formset
            }
            return render(request, 'problemas/modal_casos_alternativos.html', context)

        else:
            print("la request no es ajax")
            return HttpResponseRedirect('/')



@method_decorator([docente_required], name='dispatch')
class ActualizarOutputsAlternativos(LoginRequiredMixin, View):
    def post(self, request,**kwargs):
        print("me llego el form!!!!!",kwargs['caso_id'])
        return HttpResponseRedirect('/')


