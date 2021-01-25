from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views import View

from NiñasProject.decorators import docente_required
from clases.models import Clase
from cursos.models import Curso
from feedback.forms import OutputAlternativoModelFormSet
from feedback.models import OutputAlternativo
from problemas.models import Caso


@method_decorator([docente_required], name='dispatch')
class CasosAlternativos(LoginRequiredMixin, View):
    def get(self, request):
        if request.is_ajax():
            id_caso = request.GET.get('id')
            caso = Caso.objects.get(id=id_caso)
            # outputs_sugeridos = OutputAlternativo.objects.filter(caso=caso, agregado=False, frecuencia__gt=1)
            outputs_sugeridos = OutputAlternativo.objects.filter(caso=caso, agregado=False)
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
                messages.success(request, f"Se agregó la sugerencia en la categoría {caso.categoría}")
        return HttpResponseRedirect(
            reverse('problemas:casos-problema',
                    kwargs={'curso_id': curso.id, 'problema_id': caso.problema.id, 'result': 0}))

    # FIX: esto asume que un problema solo pertenece a un curso!
    def get_curso(self, caso, user):
        clase = caso.problema.clase # clases en la que está este problema
        return clase.curso
