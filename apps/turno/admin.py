from django.contrib import admin
from .models import Turno

class TurnoAdmin (admin.ModelAdmin):
    list_display= ('cliente', 'barbero','servicio', 'fechaHora', 'estado')
    ordering = ('-fechaHora',) 
admin.site.register(Turno, TurnoAdmin)
