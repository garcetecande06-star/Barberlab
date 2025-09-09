from django.db import models
from django.utils import timezone

estado_choices=[
    ('pendiente', 'Pendiente'),
    ('confirmado', 'Confirmado'),
    ('realizado', 'Realizado'),
    ('cancelado', 'Cancelado'),
]

class Turno(models.Model):
    cliente= models.ForeignKey ('cliente.Cliente', on_delete=models.CASCADE)
    barbero= models.ForeignKey ('barbero.Barbero', on_delete=models.CASCADE)
    servicio= models.ForeignKey ('servicio.Servicio', on_delete=models.CASCADE)
    fechaHora= models.DateTimeField(default= timezone.now)
    estado= models.CharField(max_length=10, choices=estado_choices, default='pendiente')

    def __str__(self):
        return  f"{self.cliente} - {self.servicio} con {self.barbero}"
