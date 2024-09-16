from django import forms
from django.contrib.auth.models import User
from .models import Itinerario, Actividad
from datetime import timedelta


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class ItinerarioForm(forms.ModelForm):
    class Meta:
        model = Itinerario
        fields = ['nombre', 'descripcion', 'es_publico']


class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['nombre', 'tipo_actividad', 'ubicacion', 'hora_inicio', 'duracion']
        widgets = {
            'hora_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'duracion': forms.TextInput(attrs={'placeholder': 'HH:MM'})  # Solo horas y minutos
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
            raise forms.ValidationError("La duración debe estar en el formato HH:MM.")
