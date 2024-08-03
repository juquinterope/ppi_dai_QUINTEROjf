import os
import geopandas as gpd
from django.shortcuts import render
from django.conf import settings


def explorar_municipios(request):
    # Ruta al archivo GeoJSON
    geojson_path = os.path.join(
        settings.BASE_DIR, 'data', 'municipios_antioquia.geojson')

    # Cargar el GeoDataFrame desde el archivo GeoJSON
    gdf = gpd.read_file(geojson_path)

    # Convertir el GeoDataFrame a JSON
    municipios_json = gdf.to_json()

    # Renderizar la plantilla con los datos de los municipios
    return render(request, 'exploracion/explorar_municipios.html', {'municipios_json': municipios_json})
