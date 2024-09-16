from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('itinerario/<int:itinerario_id>/',
         views.detalle_itinerario, name='detalle_itinerario'),
    path('itinerario/eliminar/<int:itinerario_id>/',
         views.eliminar_itinerario, name='eliminar_itinerario'),
    path('borrar-actividad/<int:actividad_id>/',
         views.borrar_actividad, name='borrar_actividad'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
]
