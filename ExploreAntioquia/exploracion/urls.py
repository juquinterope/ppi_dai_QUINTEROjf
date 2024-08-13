from django.urls import path
from . import views


urlpatterns = [
    path('municipios/', views.explorar_municipios, name='explorar_municipios'),
    path('municipio-detalle/<str:id>/', views.municipio_detalle, name='municipio_detalle'),
]
