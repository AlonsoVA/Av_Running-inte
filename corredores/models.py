from django.db import models  # type: ignore

# Usuario base
class Registros(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'correo'

    def __str__(self):
        return self.nombre

# Perfil extendido, vinculado por OneToOne
class Usuarioinfo(models.Model):
    usuario = models.OneToOneField(Registros, on_delete=models.CASCADE, unique=True)
    edad = models.CharField(max_length=3)
    descripcion = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='imagenes_usuarios/', blank=True, null=True)

