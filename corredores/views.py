from django.shortcuts import render, redirect # type: ignore
from corredores.models import Registros
from django.http import HttpResponse # type: ignore
from django.contrib.auth.hashers import make_password, check_password # type: ignore
from django.contrib.auth import login # type: ignore

# Create your views here.
def  home(request):
    return render(request, "home.html")

def  ruta(request):
    return render(request, "ruta.html")

def planes(request):
    return render(request, "planes.html")

def registro(request):
    if request.method == "POST":

        Nombre = request.POST.get("name")
        Correo = request.POST.get("email")
        Contraseña = request.POST.get("password")

        # Verifica en consola que los datos llegan
        print(f"Datos recibidos: {Nombre}, {Correo}, {Contraseña}")

        if Registros.objects.filter (nombre = Nombre, correo = Correo).exists():
            return HttpResponse("Usted ya esta registrado caballero")
        
        # Crea el registro
        Registros.objects.create(nombre=Nombre, correo=Correo, password=make_password(Contraseña))
    return render(request, "registro.html")

def login_view(request):
    if request.method == "POST":
        correo = request.POST.get("email")
        contraseña = request.POST.get("password")

        # Busca el usuario y verifica la contraseña (con hash)
        usuario = Registros.objects.filter(correo=correo).first()
        if usuario and check_password(contraseña, usuario.password):
            print("Usuario válido")  # ¿Se imprime esto?
            login(request, usuario) 
            return redirect('Homes')
        else:
            print("Usuario o contraseña inválidos")  # ¿O esto?
    
    return render(request, "login.html")