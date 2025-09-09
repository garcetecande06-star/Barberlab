from django.db import models
from django.contrib.auth.models import User

class Barbero (models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    nombre= models.CharField(max_length=100)
    email= models.EmailField()
    telefono= models.CharField(max_length=20)

    def __str__(self):
        return self.user.get_full_name() or self.user.username