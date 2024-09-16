from django.db import models
from django.contrib.auth.models import User


class Itinerario(models.Model):
    # Relacionamos con el modelo User
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    duracion_total = models.DurationField(null=True, blank=True)
    es_publico = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre


class Actividad(models.Model):
    itinerario = models.ForeignKey(
        Itinerario, related_name='actividades', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    # Transporte, visita, comida, etc.
    tipo_actividad = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    hora_inicio = models.DateTimeField()  # Hora de inicio de la actividad
    duracion = models.DurationField()

    def __str__(self):
        return self.nombre
