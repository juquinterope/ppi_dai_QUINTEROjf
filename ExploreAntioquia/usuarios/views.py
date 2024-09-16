from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, logout
from .forms import UserRegisterForm, ItinerarioForm, ActividadForm
# Cargar itinerarios
from .models import Itinerario, Actividad
from datetime import timedelta


def home(request):
    """Maneja la vista de itinerarios (pagina inicial)

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
    
    Returns:
        HttpResponse: Si hay una sesion de usuario iniciada, mostrara los itinerarios
        asociados.
    """
    itinerarios = None
    itinerario_form = None
    # Verifica si el usuario está autenticado
    if request.user.is_authenticated:
        # Filtra itinerarios por el usuario autenticado
        itinerarios = Itinerario.objects.filter(usuario=request.user)
        if request.method == 'POST':
            # Procesar formulario de creacion de itinerario
            itinerario_form = ItinerarioForm(request.POST)
            if itinerario_form.is_valid():
                nuevo_itinerario = itinerario_form.save(commit=False)
                nuevo_itinerario.usuario = request.user
                nuevo_itinerario.save()
                return redirect('home')
        else:
            itinerario_form = ItinerarioForm()
    return render(request, 'usuarios/home.html', {'itinerarios': itinerarios,
                                                  'itinerario_form': itinerario_form})


def detalle_itinerario(request, itinerario_id):
    """Permite ver y editar un itinerario

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        itinerario_id : El id del itinerario a cambiar, esto es manejado automaticamente
    
    Returns:
        HttpResponse: Mostrara los detalles del itinerario seleccionado y permitira
        agregar actividades al mismo.
    """
    itinerario = Itinerario.objects.get(id=itinerario_id, usuario=request.user)
    actividades = Actividad.objects.filter(itinerario=itinerario)

    if request.method == 'POST':
        actividad_form = ActividadForm(request.POST)
        if actividad_form.is_valid():
            nueva_actividad = actividad_form.save(commit=False)
            # Ajustar la duración manualmente
            duracion = actividad_form.cleaned_data['duracion']  # Obtener el valor del form
            
            # Ajustar el campo de duracion a horas,
            # Si es menos de 1 hora (3600 segundos)
            if duracion.total_seconds() < 3600:
                horas = duracion.seconds // 60  # Obtener las horas a partir de los minutos
                minutos = duracion.seconds % 60  # Obtener los minutos restantes
                nueva_actividad.duracion = timedelta(hours=horas, minutes=minutos, seconds=0)
            nueva_actividad.itinerario = itinerario
            nueva_actividad.save()
            return redirect('detalle_itinerario', itinerario_id=itinerario.id)
    else:
        actividad_form = ActividadForm()

    return render(request, 'usuarios/detalle_itinerario.html', {'itinerario': itinerario,
                                                                'actividades': actividades,
                                                                'actividad_form': actividad_form})


def eliminar_itinerario(request, itinerario_id):
    """Maneja el borrado de nuevos itinerarios

    Si la solicitud es 'POST', es decir se acepta la eliminacion, se borra el itineario 
    Si la solicitud es 'GET', es decir se cancela la eliminacion, no se borra el itineario

    Args:
        request (HttpRequest): La solicitud HTTP recibida
        itinerario_id: El itineario que se intenta eliminar

    Returns:
        HttpResponse: Redirige a la página de inicio tras un borrado exitoso o si este se cancela
    """
    itinerario = get_object_or_404(Itinerario, id=itinerario_id, usuario=request.user)

    if request.method == 'POST':
        itinerario.delete()
        return HttpResponseRedirect(reverse('home'))

    # Si se cancela la eliminacion vuelve a la vista inicial
    return render(request, 'usuarios/home.html')

def borrar_actividad(request, actividad_id):
    """Maneja el borrado de actividades

    Si la solicitud es 'POST', es decir se acepta la eliminacion, se borra la acctividad 
    Si la solicitud es 'GET', es decir se cancela la eliminacion, no se borra la actividad

    Args:
        request (HttpRequest): La solicitud HTTP recibida
        actividad_id: La actividad que se intenta eliminar

    Returns:
        HttpResponse: Redirige a la página de inicio tras un borrado exitoso o si este se cancela
    """
    # Obtiene la actividad o muestra un 404 si no existe
    actividad = get_object_or_404(Actividad, id=actividad_id)
    
    # Verifica que el usuario sea el propietario del itinerario antes de eliminar
    if actividad.itinerario.usuario == request.user:
        actividad.delete()
        messages.success(request, 'Actividad eliminada correctamente.')
    else:
        messages.error(request, 'No tienes permiso para eliminar esta actividad.')

    # Redirige a la pagina de detalles del itinerario
    return redirect('detalle_itinerario', itinerario_id=actividad.itinerario.id)


def register(request):
    """Maneja el registro de nuevos usuarios.

    Si la solicitud es 'POST', valida y guarda el nuevo usuario, y luego inicia sesión automáticamente. 
    Si la solicitud es 'GET', muestra el formulario de registro.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.

    Returns:
        HttpResponse: Redirige a la página de inicio tras un registro exitoso o muestra el formulario de registro.
    """
    # Si el formulario de login es enviado 'POST'
    if request.method == 'POST':
        # Se registra el formulario en el modelo de django,
        # el login viene predefinido
        form = UserRegisterForm(request.POST)
        # Si los datos ingresados son validos
        if form.is_valid():
            # Se guarda el objeto (sin escribirlo aun en la base de datos)
            user = form.save(commit=False)
            # Se limpia la contraseña
            user.set_password(form.cleaned_data['password'])
            # Se escribe el usuario en la base de datos
            user.save()

            # Si el registro es correcto se carga una login request de django
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'usuarios/register.html', {'form': form})


# Luego de logout se redirecciona al inicio
def logout_view(request):
    """Implementa directamente el logout de usuarios usando django

    Args:
        request(HttpRequest): Solicitud HTTP con la sesion del usuario cargada
    
    Returns:
        HttpResponse: Cierra la sesion del usuario y redirecciona a la vista inicial
    """
    logout(request)
    return redirect('home')
