from django.db import models
from django.utils import timezone

PUNTUACION_CHOICES = [
    (1, '⭐'),
    (2, '⭐⭐'),
    (3, '⭐⭐⭐'),
    (4, '⭐⭐⭐⭐'),
    (5, '⭐⭐⭐⭐⭐'),
]

class Valoracion(models.Model):
    nombre_cliente = models.CharField(max_length=100, default="anónimo")  
    barbero = models.ForeignKey('barbero.Barbero', on_delete=models.CASCADE)
    servicio = models.ForeignKey('servicio.Servicio', on_delete=models.CASCADE)
    puntuacion = models.PositiveBigIntegerField(choices=PUNTUACION_CHOICES)
    comentario = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.nombre_cliente} valoró a {self.barbero} con {self.puntuacion} estrellas"
        