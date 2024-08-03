from django.urls import path
from . import views


urlpatterns = [
    path('municipios/', views.explorar_municipios, name='explorar_municipios'),
]
