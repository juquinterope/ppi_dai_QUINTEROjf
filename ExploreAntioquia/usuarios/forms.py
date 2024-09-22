from django import forms
from django.contrib.auth.models import User
from .models import Itinerario, Actividad
from datetime import timedelta


class UserRegisterForm(forms.ModelForm):
    # Los campos originalemte aparecen en ingles, cambiemos los labels
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

    class Meta:
        model = User
        # Ajustar el idioma del formulario
        fields = ['username', 'password']
        labels = {
            'username': 'Nombre de usuario',
        }
        help_texts = {
            'username': 'Requerido. 150 caracteres o menos. Letras, números y @/./+/-/_ solamente.',
        }
        error_messages = {
            'username': {
                'required': 'Este campo es obligatorio.',
                'invalid': 'Introduce un nombre de usuario válido.',
            },
        }


class ItinerarioForm(forms.ModelForm):
    class Meta:
        model = Itinerario
        fields = ['nombre', 'descripcion', 'es_publico']


class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['nombre', 'tipo_actividad',
                  'ubicacion', 'hora_inicio', 'duracion']
        widgets = {
            'hora_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            # Solo horas y minutos
            'duracion': forms.TextInput(attrs={'placeholder': 'HH:MM'})
        }

    def clean_duracion(self):
        """Funcion auxiliar para que la duracion este en HH:MM

        Alza un error si el valor ingresado en la 'duracion' del form no esta en HH:MM
        """
        duracion = str(self.cleaned_data['duracion'])
        try:
            # Separamos en horas y minutos (vamos a despreciar los segundos)
            horas, minutos, segundos = map(int, duracion.split(':'))
            # Convertimos a timedelta
            return timedelta(hours=horas, minutes=minutos, seconds=0)
        except ValueError:
            raise forms.ValidationError(
                "La duración debe estar en el formato HH:MM.")
