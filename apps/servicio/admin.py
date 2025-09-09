from django.contrib import admin
from .models import Servicio

class ServicioAdmin(admin.ModelAdmin):
    list_display= ('nombre', 'precio')

admin.site.register(Servicio, ServicioAdmin)
