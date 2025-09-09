from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Cliente
from apps.servicio.models import Servicio
from apps.valoracion.models import Valoracion

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
        return redirect('agenda_turnos')

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
            return redirect('agenda_turnos')
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
            return render(request, self.template_name)




