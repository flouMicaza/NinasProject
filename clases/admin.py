from django.contrib import admin
from clases.models import Clase

@admin.register(Clase)
class ClaseAdmin(admin.ModelAdmin):
    base_model = Clase
    list_display = ['__str__', 'curso']
