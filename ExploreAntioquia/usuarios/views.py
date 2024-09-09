from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegisterForm
from django.contrib.auth.views import LogoutView


def home(request):
    return render(request, 'usuarios/home.html')


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
    logout(request)
    return redirect('home')
