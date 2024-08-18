from django.shortcuts import render
from decouple import config # type: ignore

# Create your views here.
def ver_turismo(request):
    places_api = config('PLACES_API')
    return render(request, 'turismo/mapa_turismo.html', {'PLACES_API': places_api})