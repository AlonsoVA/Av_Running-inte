from django.db import models # type: ignore

# Create your models here.

class Corredor(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()
    tiempo_5k = models.FloatField()

class Registros(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

        # Campos requeridos por Django
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'correo'  # Define qué campo se usará como nombre de usuario

    def __str__(self):
        return self.nombre
