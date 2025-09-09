from django.contrib import admin

class ValoracionAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'barbero', 'servicio', 'puntuacion', 'fecha')
    search_fields = ('cliente__nombre', 'barbero__nombre', 'servicio__nombre')
    ordering = ('-fecha',) 
