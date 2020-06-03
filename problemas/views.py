import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView

from NiñasProject.decorators import profesora_required
from NiñasProject.utils import get_ordered_test_feedback, get_casos_por_categoria
from clases.models import Clase
from cursos.models import Curso
from feedback.models import Feedback, TestFeedback, OutputAlternativo
from problemas.forms import ProblemaForm
from problemas.models import Problema, Caso

from scriptserver.comunication.client import Client

ComunicationClient = Client()


class ProblemasViews(LoginRequiredMixin, TemplateView):
    tab = 'enunciado'
    login_url = 'usuarios:login'
    redirect_field_name = ''
    template_name = "problemas/inicio_problemas.html"
    feedback_template_name = "problemas/inicio_problemas.html"
    feedback_error_template_name = "error.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        problema = get_object_or_404(Problema, id=self.kwargs['problema_id'])
        curso = get_object_or_404(Curso, id=self.kwargs['curso_id'])

        context['curso'] = curso
        context['problema'] = problema
        context['has_tests'] = bool(problema.tests)
        context['casos'] = get_casos_por_categoria(Caso.objects.filter(problema=problema))

        nuevos_outputs = {}
        for caso in Caso.objects.filter(problema=problema):
            nuevos_outputs[caso.id] = OutputAlternativo.objects.filter(caso=caso, agregado=False,
                                                                       frecuencia__gt=1).count()
        context['nuevos_outputs'] = nuevos_outputs

        if self.tab == 'enunciado':
            context['enunciado_active'] = 'active'
            context['casos_active'] = ''
            context['resultados_active'] = ''
        elif self.tab == 'casos':
            context['enunciado_active'] = ''
            context['casos_active'] = 'active'
            context['resultados_active'] = ''
        else:
            context['enunciado_active'] = ''
            context['casos_active'] = ''
            context['resultados_active'] = 'active'

        if self.kwargs['result'] == 1:
            feedback = Feedback.objects.filter(problema=problema).order_by('fecha_envio').last()
            context['test_feedback'] = TestFeedback.objects.filter(feedback=feedback)
            context['cantidad_buenos'] = context['test_feedback'].filter(passed='True').count()
            context['cantidad_malos'] = context['test_feedback'].filter(passed='False').count()
            context['ordered_test_feedback'] = get_ordered_test_feedback(context['test_feedback'], problema)
            context['resultados_active'] = "active"
        return context

    def post(self, request, *args, **kwargs):

        # Get assignment and post data
        problema = get_object_or_404(Problema, id=self.kwargs['problema_id'])
        curso = get_object_or_404(Curso, id=self.kwargs['curso_id'])

        if not bool(problema.tests):
            return self.handle_failed_single_response(request,
                                                      "The Assignment has no tests, talk to the course's teacher or assistants to fix this issue.",
                                                      **kwargs)

        data = request.POST.copy()

        # Get language and file from data
        lang = 'cpp'
        file = request.FILES.get('sample_code')  # Archivo que quiero testear

        # If the user didn´t uploaded a file it sends the user back to the same page
        if file is None or file.name.split('.')[-1] != 'cpp':
            context_data = self.get_context_data(**kwargs)
            context_data['file_error'] = "Debes agregar un archivo" if (
                    file is None) else "El archivo debe ser formato .cpp"
            return render(request, self.template_name, context_data)

        # Save the file in the media folder
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)

        # get the path from the media folder
        script_path = settings.MEDIA_ROOT + '/' + filename
        test_path = problema.tests.path.replace("\\", "/")

        # Send and receive data for testing.
        response = ComunicationClient.send_submission(script_path, test_path, lang)

        compiled_file = filename.split('.')[0]

        try:
            # Delete compiled file
            os.remove(compiled_file)
        except:
            pass

        if response[0] == "success":
            os.remove(script_path)
            return self.handle_successful_single_response(request, problema, response[1], file, **kwargs)
        else:
            # os.remove(script_path)
            return self.handle_failed_single_response(request, response[1], **kwargs)

    def handle_successful_single_response(self, request, problema, tests_arr, codigo_solucion, **kwargs):
        # Save tests_arr as a feedback object and a group of simple_test_feedback objects
        feedback_user = request.user
        feedback_problema = problema
        feedback_codigo = codigo_solucion
        feedback = Feedback.objects.create(user=feedback_user, problema=feedback_problema,
                                           codigo_solucion=feedback_codigo)
        self.crear_test_feedbacks(feedback, tests_arr)

        this_context = self.get_context_data(**kwargs)
        this_context['test_feedback'] = TestFeedback.objects.filter(feedback=feedback)
        this_context['ordered_test_feedback'] = get_ordered_test_feedback(this_context['test_feedback'], problema)
        this_context['cantidad_buenos'] = this_context['test_feedback'].filter(passed='True').count()
        this_context['cantidad_malos'] = this_context['test_feedback'].filter(passed='False').count()
        this_context['test_array'] = tests_arr
        this_context['resultados_active'] = "active"
        this_context['enunciado_active'] = ""
        return render(request, self.feedback_template_name, this_context)

    def crear_test_feedbacks(self, feedback, tests_arr):
        nuevos_outputs = {}
        for test in tests_arr:
            input = test[1]
            caso = Caso.objects.get(input=input, problema=feedback.problema)
            test_feedback = TestFeedback.objects.create(passed=test[0], output_obtenido=test[5], error=test[4],
                                                        caso=caso,
                                                        feedback=feedback)

            # Si no pasa el test y no tuvo error, tengo que agregar output_alternativo y asociárselo al test_feedback
            if test_feedback.passed == 0 and test_feedback.error == 0:
                output_alternativo, created = OutputAlternativo.objects.get_or_create(caso=caso,
                                                                                      output_obtenido=test_feedback.output_obtenido)
                if not created:
                    output_alternativo.frecuencia += 1
                    output_alternativo.save()

                test_feedback.output_alternativo = output_alternativo
                test_feedback.save()

    '''
    Los errrores serían si no hay tests o si no compila el código. 
    '''

    def handle_failed_single_response(self, request, error, **kwargs):
        this_context = self.get_context_data(**kwargs)
        this_context['error'] = error
        this_context['error_resumen'] = "Hubo un error al procesar tu código"
        this_context['resultados_active'] = "active"
        this_context['enunciado_active'] = ""
        return render(request, self.feedback_template_name, this_context)


@method_decorator([profesora_required], name='dispatch')
class CrearProblemasViews(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        clase_id = kwargs['clase_id']
        clase = get_object_or_404(Clase.objects.filter(id=clase_id))

        if not request.user in clase.curso.profesoras.all():
            return HttpResponseForbidden("No tienes permiso para ingresar a este curso.")

        form = ProblemaForm()
        return render(request, 'problemas/crear_problema.html', {'clase': clase, 'form': form})

    def post(self, request, **kwargs):
        clase_id = kwargs['clase_id']
        clase = get_object_or_404(Clase.objects.filter(id=clase_id))
        if not request.user in clase.curso.profesoras.all():
            return HttpResponseForbidden("No tienes permiso para ingresar a este curso.")

        form = ProblemaForm(request.POST, request.FILES)
        if form.is_valid():
            nuevo_problema = form.save()
            clase.problemas.add(nuevo_problema)
            messages.success(request, 'Se creó el problema ' + nuevo_problema.titulo)
            return HttpResponseRedirect(reverse('cursos:curso', kwargs={'curso_id': clase.curso.id}))
        return render(request, 'problemas/crear_problema.html', {'clase': clase, 'form': form})
