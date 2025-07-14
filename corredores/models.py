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

# Perfil extendido
class Usuarioinfo(models.Model):
    usuario = models.OneToOneField(Registros, on_delete=models.CASCADE, unique=True)
    edad = models.CharField(max_length=3)
    descripcion = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='imagenes_usuarios/', blank=True, null=True)


class MensajeChat(models.Model):
    usuario = models.ForeignKey(Usuarioinfo, on_delete=models.CASCADE)
    mensaje_usuario = models.TextField()
    mensaje_respuesta = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    
class Ruta(models.Model):
    usuario = models.ForeignKey(Registros, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    nota = models.TextField(blank=True)
    distancia = models.FloatField(default=0)
    coordenadas = models.JSONField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

