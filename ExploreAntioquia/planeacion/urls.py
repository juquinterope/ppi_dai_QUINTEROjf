from django.urls import path
from . import views


urlpatterns = [
    path('', views.planear_viaje, name='planear_viaje'),
]
