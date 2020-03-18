import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView

from cursos.models import Curso
from problemas.models import Problema

from scriptserver.comunication.client import Client

ComunicationClient = Client()

class ProblemasViews(LoginRequiredMixin, TemplateView):
    login_url = 'usuarios:login'
    redirect_field_name = ''
    template_name = "problemas/inicio_problemas.html"
    feedback_template_name = "problemas/feedback_page.html"
    feedback_error_template_name = "problemas/feedback_error.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        problema = get_object_or_404(Problema, id=self.kwargs['problema_id'])
        curso = get_object_or_404(Curso,id=self.kwargs['curso_id'])

        context['curso'] = curso
        context['problema'] = problema
        context['has_tests'] = bool(problema.tests)

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
        lang = 'python3'
        file = request.FILES.get('sample_code')

        # If the user didn´t uploaded a file it sends the user back to the same page
        if file == None:
            return render(request, self.template_name, self.get_context_data(**kwargs))

        # Save the file in the media folder
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)

        # get the path from the media folder
        script_path = os.getcwd().replace("\\", "/") + "/media/" + filename
        test_path = problema.tests.path.replace("\\", "/")

        if data["submission_type"] == "single":

            # Send and receive data for testing
            response = ComunicationClient.send_submission(script_path, test_path, lang)

            # Delete the source code file from the media folder
            os.remove('media/' + filename)

            if response[0] == "success":
                return self.handle_successful_single_response(request, problema, response[1], **kwargs)
            else:
                return self.handle_failed_single_response(request, response[1], **kwargs)

        elif data["submission_type"] == "multiple":

            '''SaveScriptProcess(request.user.account, assignment, lang, ComunicationClient, script_path,
                              test_path).start()

            this_context = self.get_context_data()

            return render(request, self.template_name, this_context)'''
        else:

            # Delete the source code file from the media folder
            os.remove('media/' + filename)

            raise Exception("Unidentified submission")


    def handle_successful_single_response(self, request, assignment, tests_arr, **kwargs):
        # Save tests_arr as a feedback object and a group of simple_test_feedback objects
        feedback_user = request.user
        feedback_assignment = assignment
        feedback_date = timezone.now()


        this_context = self.get_context_data(**kwargs)
        this_context['feedback_user'] = feedback_user
        this_context['feedback_assignment'] = feedback_assignment
        this_context['feedback_date'] = feedback_date
        this_context['test_array'] = tests_arr
        return render(request, self.feedback_template_name, this_context)

    def handle_failed_single_response(self,request):
        return render(request,self.feedback_error_template_name)
