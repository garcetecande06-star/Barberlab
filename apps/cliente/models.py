from django.db import models
from django.contrib.auth.models import User

class Cliente (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    nombre= models.CharField(max_length=100)
    email= models.EmailField()
    telefono= models.CharField(max_length=20)
    contraseña = models.CharField(max_length=128, default='12345')

    def __str__(self):
        return self.nombre