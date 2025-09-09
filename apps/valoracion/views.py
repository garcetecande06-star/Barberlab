from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Valoracion

class NuevaValoracionView(CreateView):
    model = Valoracion
    fields = ['nombre_cliente', 'barbero', 'servicio', 'puntuacion', 'comentario']
    template_name = 'nuevaValoracion.html'
    success_url = reverse_lazy('index')  # Cambia 'index' por tu vista principal


