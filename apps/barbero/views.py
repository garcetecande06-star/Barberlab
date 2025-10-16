from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from apps.turno.models import Turno
from apps.barbero.models import Barbero

class LoginStaffView(View):
    template_name = 'Inicio_De_Sesion_Barberos.html'  

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        #Se obtienen los datos del formulario
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            #Si el usuario existe y es staff
            if user.is_staff:
                #Se inicia sesión
                login(request, user)
                #Se redirige a la agenda
                return redirect('agenda')  # Redirige a la agenda
            else:
                #El usuario no es staff y no tiene acceso
                messages.error(request, "No tienes permisos para acceder.")
        else:
            #Usuario o contraseña incorrectos
            messages.error(request, "Usuario o contraseña incorrectos.")
        #Luego de un error muestra el formulario de nuevo
        return render(request, self.template_name)


class AgendaTurnosView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'agendaBarbero.html'
    login_url = 'login_staff' 

    def test_func(self):
        return self.request.user.is_staff  # Solo staff puede acceder

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