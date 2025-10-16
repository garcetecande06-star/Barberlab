from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from datetime import datetime, date
from django.utils import timezone  # Importación clave
from .models import Cliente
from apps.servicio.models import Servicio
from apps.barbero.models import Barbero
from apps.valoracion.models import Valoracion
from apps.turno.models import Turno
from django import forms


# ------------------ Index ------------------
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['servicios'] = Servicio.objects.all()
        context['valoraciones'] = Valoracion.objects.select_related('barbero', 'servicio').all()
        return context


# ------------------ Registro ------------------
class RegistroClienteView(View):
    template_name = 'registro.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')

        if User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe")
            return render(request, self.template_name)

        if User.objects.filter(email=email).exists():
            messages.error(request, "El email ya está registrado")
            return render(request, self.template_name)

        user = User.objects.create_user(username=username, password=password, email=email)
        Cliente.objects.create(user=user, nombre=nombre, email=email, telefono=telefono)

        login(request, user)
        return redirect('turnosCliente')


# ------------------ Login ------------------
class LoginClienteView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                nombre_cliente = user.cliente.nombre
                login(request, user)
                return redirect('turnosCliente')
            except Cliente.DoesNotExist:
                # Esto manejaría el caso donde el User existe, pero no el Cliente asociado
                messages.error(request, "Usuario o contraseña incorrectos")
                return render(request, self.template_name)
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
            return render(request, self.template_name)


# ------------------ TurnosCliente ------------------
class TurnosClienteView(LoginRequiredMixin, TemplateView):
    template_name = 'turnosCliente.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.request.user, 'cliente'):
            context['turnos'] = Turno.objects.filter(
                cliente=self.request.user.cliente
            ).order_by('fechaHora')
        else:
            context['turnos'] = Turno.objects.none()
        return context


# ------------------ Formulario ReservarTurno ------------------

HORARIOS_FIJOS = [
    ('09:00', '09:00 AM'),
    ('10:00', '10:00 AM'),
    ('11:00', '11:00 AM'),
    ('12:00', '12:00 PM'),
    ('13:00', '01:00 PM'),
    ('14:00', '02:00 PM'),
]

class TurnoForm(forms.Form):
    barbero = forms.ModelChoiceField(queryset=Barbero.objects.all())
    servicio = forms.ModelChoiceField(queryset=Servicio.objects.all())
    fecha = forms.DateField(
        label='Fecha',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'min': date.today().strftime('%Y-%m-%d')  
        }),
    )
    hora = forms.ChoiceField(choices=HORARIOS_FIJOS, label="Hora")

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora_str = cleaned_data.get('hora')

        if fecha and hora_str:
            hora = datetime.strptime(hora_str, '%H:%M').time()
            
            naive_fecha_hora = datetime.combine(fecha, hora)
            
            fecha_hora = timezone.make_aware(naive_fecha_hora)

            if fecha_hora < timezone.now():
                raise forms.ValidationError("No podés reservar turnos en el pasado.")

            cleaned_data['fechaHora'] = fecha_hora
        return cleaned_data

# ------------------ ReservarTurnoView ------------------
class reservarTurnoView(LoginRequiredMixin, View):
    template_name = 'reservarTurno.html'
    success_url = reverse_lazy('turnosCliente')

    def get(self, request):
        form = TurnoForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = TurnoForm(request.POST)
        if form.is_valid():
            cliente = Cliente.objects.get(user=request.user)
            fechaHora = form.cleaned_data['fechaHora']
            barbero = form.cleaned_data['barbero']

            # Validar turno del cliente
            if Turno.objects.filter(cliente=cliente, fechaHora=fechaHora).exists():
                form.add_error(None, "Ya tenés un turno reservado para ese horario.")
                return render(request, self.template_name, {'form': form})

            # Validar turno del barbero
            if Turno.objects.filter(barbero=barbero, fechaHora=fechaHora).exists():
                form.add_error(None, "El barbero ya tiene un turno reservado en ese horario.")
                return render(request, self.template_name, {'form': form})

            turno = Turno(
                cliente=cliente,
                barbero=barbero,
                servicio=form.cleaned_data['servicio'],
                fechaHora=fechaHora,
                estado='pendiente'
            )
            turno.save()
            return redirect(self.success_url)

        return render(request, self.template_name, {'form': form})


# ------------------ EliminarTurno ------------------
class eliminarTurnoView(LoginRequiredMixin, DeleteView):
    model = Turno
    template_name = "eliminarTurno.html"
    success_url = reverse_lazy('turnosCliente')