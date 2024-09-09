import os
import geopandas as gpd  # type: ignore
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings


def explorar_municipios(request):
    """Vista para explorar los municipios de Antioquia utilizando datos 
    geoespaciales.

    Esta función carga un archivo GeoJSON que contiene información 
    geográfica sobre los municipios de Antioquia, lo convierte a 
    formato JSON, y luego renderiza una plantilla HTML pasando 
    los datos para su visualización.

    Args:
        request (HttpRequest): El objeto de solicitud HTTP.

    Returns:
        HttpResponse: Respuesta que renderiza la plantilla 
                      'exploracion/explorar_municipios.html' con los 
                      datos de los municipios en formato JSON.
    """
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
    """Vista para obtener los detalles de un municipio específico de Antioquia.

    Esta función carga un archivo GeoJSON que contiene la información 
    geográfica y descriptiva de los municipios de Antioquia, busca el 
    municipio correspondiente al `id` proporcionado, y devuelve la 
    información en formato JSON.

    Args:
        request (HttpRequest): El objeto de solicitud HTTP.
        id (str): El nombre del municipio cuyo detalle se desea obtener.
                  Los espacios en blanco deben estar codificados como '%20'.

    Returns:
        JsonResponse: Un objeto JSON que contiene el nombre y la descripción 
                      del municipio solicitado.
    """
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
