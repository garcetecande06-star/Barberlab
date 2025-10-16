from django.contrib import admin
from django.urls import path
from apps.cliente.views import IndexView, RegistroClienteView, LoginClienteView, TurnosClienteView, reservarTurnoView, eliminarTurnoView
from apps.barbero.views import AgendaTurnosView, acceso_generico_view 
from apps.valoracion.views import NuevaValoracionView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('nuevaValoracion/', NuevaValoracionView.as_view(), name='nuevaValoracion'),
    
    path('acceso/', acceso_generico_view, name='acceso_gen'),
    
    # RUTA DE DESTINO: La agenda
    path('agenda/', AgendaTurnosView.as_view(), name='agenda_turnos'),
    
    path('login/', LoginClienteView.as_view(), name='login'),
    path('registro/', RegistroClienteView.as_view(), name='logout'),
    path('turnoCliente/',TurnosClienteView.as_view(), name='turnosCliente' ),
    path('reservarTurno/', reservarTurnoView.as_view(), name='turno_nuevo'),
    path('turno/<int:pk>/delete/', eliminarTurnoView.as_view(), name='eliminarTurno'),
]