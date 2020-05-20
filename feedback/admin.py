from django.contrib import admin

# Register your models here.
from django.contrib import admin
from feedback.models import Feedback, TestFeedback, OutputAlternativo


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    base_model = Feedback
    list_display = ['user', 'problema', 'fecha_envio']

@admin.register(TestFeedback)
class TestFeedbackAdmin(admin.ModelAdmin):
    base_model = TestFeedback
    list_display = ['__str__','caso', 'feedback', 'output_obtenido']

@admin.register(OutputAlternativo)
class OutputAlternativoAdmin(admin.ModelAdmin):
    base_model = OutputAlternativo
    list_display = ['__str__','caso', 'output_obtenido','frecuencia']