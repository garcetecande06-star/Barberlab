from django.contrib import admin
from django.urls import path
from apps.cliente.views import IndexView, RegistroClienteView, LoginClienteView
from apps.valoracion.views import NuevaValoracionView
from apps.turno.views import AgendaTurnosView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('nuevaValoracion/', NuevaValoracionView.as_view(), name='nuevaValoracion'),
    path('agenda/', AgendaTurnosView.as_view(), name='agenda_turnos'),
    path('login/', LoginClienteView.as_view(), name='login'),
    path('registro/', RegistroClienteView.as_view(), name='logout'),
]
