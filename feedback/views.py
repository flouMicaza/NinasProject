from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from NiñasProject.decorators import docente_required
from feedback.forms import OutputAlternativoModelFormSet
from feedback.models import OutputAlternativo, Feedback, TestFeedback
from problemas.models import Caso


@method_decorator([docente_required], name='dispatch')
class CasosAlternativos(LoginRequiredMixin, View):
    def get(self, request):
        if request.is_ajax():
            id_caso = request.GET.get('id')
            problema = request.GET.get('problema')

            caso = Caso.objects.get(id=id_caso)

            # outputs_sugeridos = OutputAlternativo.objects.filter(caso=caso, agregado=False, frecuencia__gt=1)
            outputs_sugeridos = OutputAlternativo.objects.filter(caso=caso, agregado=False)
            outputs_agregados = OutputAlternativo.objects.filter(caso=caso, agregado=True)

            formset = OutputAlternativoModelFormSet(queryset=outputs_sugeridos)

            ultimos_feedbacks = []
            for feedback in Feedback.objects.filter(problema=problema).values('user').annotate(
                    ultima_fecha=Max('fecha_envio')):
                ultimo = Feedback.objects.get(problema=problema, user=feedback['user'],
                                              fecha_envio=feedback['ultima_fecha'])
                ultimos_feedbacks.append(ultimo)

            tests_caso = TestFeedback.objects.filter(caso=caso).order_by('-feedback__fecha_envio')

            context = {
                'id_caso': id_caso,
                'caso': caso,
                'outputs_sugeridos': outputs_sugeridos,
                'outputs_agregados': outputs_agregados,
                'formset': formset,
                'tests_caso': tests_caso
            }
            return render(request, 'problemas/modal_casos_alternativos.html', context)

        # TODO: si no es ajax que se debería hacer?
        else:
            print("la request no es ajax")
            return HttpResponseRedirect('/')


@method_decorator([docente_required], name='dispatch')
class ActualizarOutputsAlternativos(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        id_caso = kwargs['caso_id']
        caso = Caso.objects.get(id=id_caso)
        curso = self.get_curso(caso, request.user)
        #outputs_sugeridos = OutputAlternativo.objects.filter(caso=caso, agregado=False, frecuencia__gt=1)
        outputs_sugeridos = OutputAlternativo.objects.filter(caso=caso, agregado=False)
        formset = OutputAlternativoModelFormSet(request.POST, queryset=outputs_sugeridos)
        if formset.is_valid():
            print("Formset valid!")
            instances = formset.save()
            for inst in instances:
                print(inst)
                inst.agregado = True
                inst.save()
        return HttpResponseRedirect(
            reverse('problemas:casos-problema',
                    kwargs={'curso_id': curso.id, 'problema_id': caso.problema.id, 'result': 0}))

    # FIX: esto asume que un problema solo pertenece a un curso!
    def get_curso(self, caso, user):
        clase = caso.problema.clase # clases en la que está este problema
        return clase.curso
