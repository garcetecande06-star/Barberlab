from django.views.generic import TemplateView
from django.shortcuts import render 
from apps.turno.models import Turno
from apps.barbero.models import Barbero

class AgendaTurnosView(TemplateView):
    template_name = 'agendaBarbero.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        barbero_id = self.request.GET.get('barbero')

        if barbero_id and barbero_id.isdigit():
            context['turnos'] = Turno.objects.filter(barbero_id=barbero_id).order_by('fechaHora')
            context['barbero_seleccionado'] = int(barbero_id)
        else:
            context['turnos'] = Turno.objects.all().order_by('fechaHora')
            context['barbero_seleccionado'] = None

        context['barberos'] = Barbero.objects.all()
        return context

def acceso_generico_view(request):
    return render(request, 'Inicio_De_Secion_Barberos.html')