import os
import geopandas as gpd # type: ignore
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings


def explorar_municipios(request):
    # Ruta al archivo GeoJSON
    geojson_path = os.path.join(
        settings.BASE_DIR, 'data', 'municipios_antioquia_actualizado.geojson')

    # Cargar el GeoDataFrame desde el archivo GeoJSON
    gdf = gpd.read_file(geojson_path)

    # Convertir el GeoDataFrame a JSON
    municipios_json = gdf.to_json()

    # Renderizar la plantilla con los datos de los municipios
    return render(request, 'exploracion/explorar_municipios.html', {'municipios_json': municipios_json})


def municipio_detalle(request, id):
    # Ruta al archivo GeoJSON
    geojson_path = os.path.join(
        settings.BASE_DIR, 'data', 'municipios_antioquia_actualizado.geojson')

    # Cargar el GeoDataFrame desde el archivo GeoJSON
    gdf = gpd.read_file(geojson_path)

    # Codificar los espacios de las url: %20 == ' '
    id = id.replace('%20', ' ')

    # Obtener información del municipio seleccionado
    # Obtener solo la fila del municipio de interes
    municipio = gdf[gdf['Nombre Municipio'] == id].iloc[0]
    municipio_info = {
        'nombre': municipio['Nombre Municipio'],
        'descripcion': municipio['Descripcion']
    }

    # Devolver los datos como JSON
    return JsonResponse(municipio_info)
