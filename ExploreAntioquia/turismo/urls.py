from django.urls import path
from . import views


urlpatterns = [
    path('', views.ver_turismo, name='turismo'),
]
