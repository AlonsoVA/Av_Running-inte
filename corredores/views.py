from django.shortcuts import render, redirect
from corredores.models import Registros, Usuarioinfo
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages  # Opcional, para mensajes flash


def home(request):
    return render(request, "home.html")


def ruta(request):
    return render(request, "ruta.html")


def planes(request):
    return render(request, "planes.html")


def rutapre(request):
    return render(request, "rutaspre.html")

def logout_view(request):
    request.session.flush()
    messages.success(request, "Sesión cerrada con éxito.")
    return redirect('login')


def home2(request):
    usuario_id = request.session.get('usuario_id')

    if not usuario_id:
        return redirect('login')

    try:
        usuario_registro = Registros.objects.get(id=usuario_id)
        usuario_info = Usuarioinfo.objects.get(usuario=usuario_registro)
    except (Registros.DoesNotExist, Usuarioinfo.DoesNotExist):
        request.session.flush()
        return redirect('login')

    return render(request, 'home2.html', {
        'usuario_registro': usuario_registro,
        'usuario': usuario_info
    })


def registro(request):
    if request.session.get('usuario_id'):
        print("Usuario ya logueado, redirigiendo a Home2...")
        return redirect('Home2')

    if request.method == "POST":
        nombre = request.POST.get("name")
        correo = request.POST.get("email")
        contraseña = request.POST.get("password")

        print(f"Datos recibidos -> Nombre: {nombre}, Correo: {correo}, Contraseña: {contraseña}")

        if not nombre or not correo or not contraseña:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('registro')

        if Registros.objects.filter(correo=correo).exists():
            messages.error(request, "Este correo ya está registrado.")
            return redirect('registro')

        try:
            usuario = Registros.objects.create(
                nombre=nombre,
                correo=correo,
                password=make_password(contraseña)
            )

            print(f"Usuario creado con ID: {usuario.id}")

            # Evita errores si se está intentando guardar edad, descripcion o imagen que no son del formulario actual
            Usuarioinfo.objects.create(
                usuario=usuario,
                edad="0",  # Valores por defecto
                descripcion="",
                imagen=None
            )

            request.session['usuario_id'] = usuario.id
            request.session['nombre_usuario'] = usuario.nombre

            print(f"Sesión iniciada con ID: {request.session['usuario_id']}")
            return redirect('Home2')

        except Exception as e:
            print("Error al registrar:", e)
            messages.error(request, "Hubo un error al registrarse.")
            return redirect('registro')

    return render(request, "registro.html")



def login_view(request):
    if request.session.get('usuario_id'):
        return redirect('Home2')  # Ya logueado, redirigir al home
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(f"Intento de login con correo: {email}")

        try:
            usuario = Registros.objects.get(correo=email)
        except Registros.DoesNotExist:
            messages.error(request, "Correo o contraseña incorrectos.")
            return render(request, 'login.html')

        if check_password(password, usuario.password):
            # Login correcto
            request.session['usuario_id'] = usuario.id
            request.session['nombre_usuario'] = usuario.nombre
            print(f"Login exitoso, sesión iniciada para usuario ID: {usuario.id}")
            return redirect('Home2')
        else:
            messages.error(request, "Correo o contraseña incorrectos.")
            return render(request, 'login.html')

    return render(request, 'login.html')



def usuario(request):
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        return redirect("login")

    if request.method == "POST":
        edad = request.POST.get("edad")
        descripcion = request.POST.get("descripcion")
        imagen = request.FILES.get("imagen")

        try:
            usuario = Registros.objects.get(id=usuario_id)
        except Registros.DoesNotExist:
            return HttpResponse("Usuario no encontrado")

        Usuarioinfo.objects.update_or_create(
            usuario=usuario,
            defaults={
                'edad': edad,
                'descripcion': descripcion,
                'imagen': imagen
            }
        )
        return redirect('Home2')

    return render(request, "usuario.html")


def mostrar_usuario(request, id):
    usuario = Usuarioinfo.objects.get(id=id)
    return render(request, "infouser.html", {'usuario': usuario})
