from django.contrib import admin
from .models import Barbero

class BarberoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'telefono')

admin.site.register(Barbero,BarberoAdmin)