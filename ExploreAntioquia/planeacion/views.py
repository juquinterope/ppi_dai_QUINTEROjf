import os
from django.shortcuts import render
import geopandas as gpd  # type: ignore
from django.conf import settings
from .scripts.temperatura_municipios import municipios_mas_cercanos, obtener_datos_climaticos, mapa_calor
from .scripts.places_api import search_places


def planear_viaje(request):
    # Ruta al archivo GeoJSON
    geojson_path = os.path.join(
        settings.BASE_DIR, 'data', 'municipios_antioquia_actualizado.geojson')

    # Cargar el GeoDataFrame desde el archivo GeoJSON
    gdf = gpd.read_file(geojson_path)
    # Extraer la columna "Nombre Municipio"
    municipios = gdf['Nombre Municipio'].tolist()
    # Si no se consulta un municipio, no hay imagen
    mapa_calor_base64 = False
    # Si no se consulta municipio, no hay restaurantes
    restaurantes = False
    nombre_municipio = False

    # Si se selecciona un municipio y se envía el formulario
    if request.method == 'POST':
        nombre_municipio = request.POST.get('municipio')

        # Manejar el caso donde no se seleccionó un municipio válido
        if nombre_municipio == '-':
            return render(request, 'planeacion/planear_viaje.html', {'municipios': municipios,
                                                                     'mapa_calor_base64': mapa_calor_base64,
                                                                     'restaurantes': restaurantes,
                                                                     'nombre_municipio': nombre_municipio})

        # Reproyectar a un sistema de coordenadas proyectado (UTM, por ejemplo EPSG:3116 para Colombia)
        gdf = gdf.to_crs(epsg=3116)
        # La funcion municipios_mas_cercanos devuelve un dataframe
        municipios_cercanos = municipios_mas_cercanos(nombre_municipio, gdf)
        # Capturar latitud y longitud de municipio de interes
        lat, lon = municipios_cercanos.loc[municipios_cercanos['Nombre Municipio']
                                           == nombre_municipio].iloc[0][['Latitud', 'Longitud']]

        # Buscar restaurantes en el municipio
        restaurantes = search_places(lat, lon, place_type='restaurant')

        # A los municipios_mas_cercanos devueltos, buscaremos su temperatura actual
        municipios_cercanos['temperatura'] = municipios_cercanos.apply(
            lambda x: obtener_datos_climaticos(
                x['Latitud'], x['Longitud'])['temperatura'],
            axis=1)

        # Volvemos a convertir el dataframe a geodataframe para usar la funcion mapa_calor()
        gdf = gpd.GeoDataFrame(
            municipios_cercanos,
            geometry=gpd.points_from_xy(
                municipios_cercanos.Longitud, municipios_cercanos.Latitud)
        )
        # Asignar el CRS inicial (WGS 84)
        # EPSG:4326 es para coordenadas geográficas (lat/lon)
        gdf = gdf.set_crs(epsg=4326)

        # Reproyectar a un CRS métrico adecuado
        gdf = gdf.to_crs(epsg=3116)
        # La funcion devuelve la imagen en bytes_base64
        mapa_calor_base64 = mapa_calor(gdf)

    return render(request, 'planeacion/planear_viaje.html', {'municipios': municipios,
                                                             'mapa_calor_base64': mapa_calor_base64,
                                                             'restaurantes': restaurantes,
                                                             'nombre_municipio': nombre_municipio})
