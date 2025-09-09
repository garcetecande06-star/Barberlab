from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Turno

class AgendaTurnosView(TemplateView):
    template_name = 'agenda.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['turnos'] = Turno.objects.all().order_by('fechaHora')
        return context

