from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cliente
from apps.servicio.models import Servicio
from apps.valoracion.models import Valoracion
from apps.turno.models import Turno

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

        # Crear User con contraseña encriptada
        user = User.objects.create_user(username=username, password=password, email=email)
        # Crear Cliente vinculado
        Cliente.objects.create(user=user, nombre=nombre, email=email, telefono=telefono)

        # Loguear automáticamente
        login(request, user)
        messages.success(request, "Registro exitoso")
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
            login(request, user)
            messages.success(request, f"Bienvenido, {user.cliente.nombre}")
            return redirect('turnosCliente')
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

# ------------------ ReservarTurno ------------------
class reservarTurnoView(LoginRequiredMixin, CreateView):
    model = Turno
    fields = ['barbero', 'servicio', 'fechaHora']  # Cliente se asigna automáticamente
    template_name = 'reservarTurno.html'
    success_url = reverse_lazy('turnosCliente')

    def form_valid(self, form):
        try:
            form.instance.cliente = Cliente.objects.get(user=self.request.user)
        except Cliente.DoesNotExist:
            form.add_error(None, "No se encontró un perfil de cliente para este usuario.")
            return self.form_invalid(form)
        return super().form_valid(form)

# ------------------ Cancelar/Eliminar Turno ------------------
class eliminarTurnoView(LoginRequiredMixin, DeleteView):
    model = Turno
    template_name = "eliminarTurno.html"
    success_url = reverse_lazy('turnosCliente')
