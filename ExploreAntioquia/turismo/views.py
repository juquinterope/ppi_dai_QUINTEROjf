import os
import geopandas as gpd # type: ignore
from django.shortcuts import render
from django.conf import settings
from decouple import config # type: ignore
from .scripts.puntos_turisticos import map_places

# Create your views here.
def ver_turismo(request):
    places_api = config('PLACES_API')
    # lat = 6.2476376
    # lng = -75.5658153
    # Ruta al archivo GeoJSON
    geojson_path = os.path.join(
        settings.BASE_DIR, 'data', 'municipios_antioquia_actualizado.geojson')

    # Cargar el GeoDataFrame desde el archivo GeoJSON
    gdf = gpd.read_file(geojson_path)
    # Extraer la columna "Nombre Municipio"
    municipios = gdf['Nombre Municipio'].tolist()
    
    if request.method == 'POST':
        nombre_municipio = str(request.POST.get('municipio'))

        # Manejar el caso donde no se seleccionó un municipio válido
        if nombre_municipio == '-':
            return render(request, 'turismo/mapa_turismo.html', {'PLACES_API': places_api,
                                                             'pois': False,
                                                             'center': False,
                                                             'municipios': municipios,
                                                             'formulario': True})
        
        # Filtra el GeoDataFrame para encontrar la fila con el nombre del municipio
        municipio = gdf[gdf['Nombre Municipio'] == nombre_municipio]
        # Asegúrate de que el municipio existe en el GeoDataFrame
        if not municipio.empty:
            lat = municipio['Latitud'].values[0]
            lng = municipio['Longitud'].values[0]
        places = map_places(lat, lng)
        # print(places)
        return render(request, 'turismo/mapa_turismo.html', {'PLACES_API': places_api,
                                                             'pois': places,
                                                             'center': {"lat": lat, "lng": lng},
                                                             'municipios': municipios,
                                                             'formulario': False})
    
    return render(request, 'turismo/mapa_turismo.html', {'PLACES_API': places_api,
                                                         'pois': False,
                                                         'center': False,
                                                         'municipios': municipios,
                                                         'formulario': True})
