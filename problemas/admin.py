from django.contrib import admin
from problemas.models import Problema, Caso

admin.site.register(Problema)

@admin.register(Caso)
class CasoAdmin(admin.ModelAdmin):
    base_model = Caso
    list_display = ['__str__', 'categoría','input','problema', 'output_esperado']
