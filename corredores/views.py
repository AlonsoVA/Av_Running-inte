from django.shortcuts import render, redirect
from .models import MensajeChat, Usuarioinfo
from corredores.models import Registros, Usuarioinfo, Ruta, MensajeChat
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages  # Opcional, para mensajes flash
import json
from django.shortcuts import get_object_or_404
import xml.etree.ElementTree as ET
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def chat_corredor(request):
    if request.method == "POST":
        data = json.loads(request.body)
        mensaje_usuario = data.get('mensaje')
        usuario_id = data.get('usuario_id')

        # Buscamos el usuario de Registros
        usuario_registro = Registros.objects.get(id=usuario_id)
        # Buscamos info extendida, si existe
        usuario_info = Usuarioinfo.objects.filter(usuario=usuario_registro).first()

        # Si no existe Usuarioinfo, puedes usar usuario_registro para crear mensaje o manejarlo
        usuario_para_mensaje = usuario_info if usuario_info else usuario_registro

        if "ruta" in mensaje_usuario.lower():
            respuesta = "Recuerda que puedes ver tus rutas guardadas en la sección de perfil, ¡mantén tu constancia!"
        elif "ritmo cardíaco" in mensaje_usuario.lower():
            respuesta = "Tu ritmo cardíaco ideal está entre 120 y 150 bpm para entrenamientos moderados."
        else:
            respuesta = "¡Hola! Soy tu asistente de carrera. ¿Quieres consejos para mejorar o ver tu progreso?"

        MensajeChat.objects.create(
            usuario=usuario_para_mensaje,
            mensaje_usuario=mensaje_usuario,
            mensaje_respuesta=respuesta
        )

        return JsonResponse({"respuesta": respuesta})

    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    return render(request, "chat_gpt_corredor.html", {
        "usuario_id": usuario_id
    })




def home(request):
    return render(request, "home.html")


def cargaruta(request):
    return render(request, "cargaruta.html")

def competencia(request):
    return render(request, "competencia.html")

def ruta(request):
    return render(request, "ruta.html")

def rutas(request):
    return render(request, "rutas.html")


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
    except Registros.DoesNotExist:
        request.session.flush()
        return redirect('login')

    # Buscar info extendida, si existe
    usuario_info = Usuarioinfo.objects.filter(usuario=usuario_registro).first()

    return render(request, 'home2.html', {
        'usuario_registro': usuario_registro,
        'usuario': usuario_info  # Puede ser None, está bien
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

            # Iniciar sesión del nuevo usuario
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


def guardar_ruta(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nombre = data.get('nombre')
        nota = data.get('nota', '')
        distancia = data.get('distancia', 0)
        coordenadas = data.get('coordenadas', [])
        usuario_id = request.session.get('usuario_id')

        if not usuario_id:
            return JsonResponse({'ok': False, 'error': 'Usuario no autenticado'})

        if not nombre or not coordenadas:
            return JsonResponse({'ok': False, 'error': 'Datos incompletos'})

        usuario = get_object_or_404(Registros, id=usuario_id)

        ruta = Ruta(
            usuario=usuario,
            nombre=nombre,
            nota=nota,
            distancia=distancia,
            coordenadas=coordenadas
        )
        ruta.save()

        return JsonResponse({'ok': True, 'id': ruta.id})

    return JsonResponse({'ok': False, 'error': 'Método no permitido'})


def exportar_gpx(request, ruta_id):
    ruta = get_object_or_404(Ruta, pk=ruta_id)
    coords = ruta.coordenadas

    gpx = ET.Element('gpx', version="1.1", creator="RunnersApp")
    trk = ET.SubElement(gpx, 'trk')
    name = ET.SubElement(trk, 'name')
    name.text = ruta.nombre
    trkseg = ET.SubElement(trk, 'trkseg')

    for punto in coords:
        trkpt = ET.SubElement(trkseg, 'trkpt', lat=str(punto['lat']), lon=str(punto['lng']))

    xml_str = ET.tostring(gpx, encoding='utf-8', xml_declaration=True)

    response = HttpResponse(xml_str, content_type='application/gpx+xml')
    response['Content-Disposition'] = f'attachment; filename="{ruta.nombre}.gpx"'
    return response


def tus_rutas(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    rutas_usuario = Ruta.objects.filter(usuario_id=usuario_id).order_by('-fecha_creacion')

    rutas_json = []
    for ruta in rutas_usuario:
        rutas_json.append({
            'id': ruta.id,
            'nombre': ruta.nombre,
            'nota': ruta.nota,
            'distancia': ruta.distancia,
            'coordenadas': ruta.coordenadas,
        })

    return render(request, 'tus_rutas.html', {
        'rutas': rutas_usuario,
        'rutas_json': rutas_json
    })



