import os
import geopandas as gpd # type: ignore
from django.shortcuts import render
from django.conf import settings
from decouple import config # type: ignore
from .scripts.puntos_turisticos import map_places
from .scripts.opiniones_hoteles import obtener_hoteles_cercanos, reviews, cluster_opinions_by_hotel


# Create your views here.
def ver_turismo(request):
    places_api = config('PLACES_API')
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


def ver_hoteles(request):
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
            return render(request, 'turismo/mapa_turismo.html', {'municipios': municipios})
        
        # Filtra el GeoDataFrame para encontrar la fila con el nombre del municipio
        municipio = gdf[gdf['Nombre Municipio'] == nombre_municipio]
        # Asegúrate de que el municipio existe en el GeoDataFrame
        if not municipio.empty:
            lat = float(municipio['Latitud'].values[0])
            lng = float(municipio['Longitud'].values[0])

        # Llamar a la funcion que busca hoteles cercanos
        hoteles = obtener_hoteles_cercanos(lat, lng, nombre_municipio)
        opiniones = []
        for hotel in hoteles:
            # Ver la review de cada hotel
            review = reviews(str(hotel['id']), hotel['nombre'], hotel['direccion'])
            opiniones.append(review)

        # Agrupar opiniones por temas
        opiniones = cluster_opinions_by_hotel(opiniones)
        hoteles_clusterizados = {}
        # Palabras clave de las opiniones
        all_keywords = set()

        for hotel in opiniones:
            hotel_nombre = hotel['nombre']
            hotel_direccion = hotel['direccion']
            hotel_opiniones = hotel['reviews']
            
            for opinion in hotel_opiniones:
                all_keywords.update(opinion['cluster_keywords'])
            hoteles_clusterizados[hotel_nombre] = {
                'direccion': hotel_direccion,
                'opiniones': hotel_opiniones
            }

        request.session['hoteles'] = hoteles_clusterizados
        request.session['unique_keywords'] = list(all_keywords)

        return render(request, 'turismo/hoteles.html', {'hoteles': hoteles_clusterizados,
                                                        'unique_keywords': list(all_keywords),
                                                        'keyword': False,
                                                        'municipios': municipios})

    elif request.method == 'GET' and request.GET.get('keyword'):
        # Recuperar la información de la sesión en lugar de recalcular
        hoteles = request.session.get('hoteles')
        unique_keywords = request.session.get('unique_keywords', [])
        # Tomar la opcion de filtrado
        keyword = request.GET.get('keyword', False)

        if keyword:
            # Filtrar las opiniones por la keyword seleccionada
            filtered_hoteles = {}
            for hotel_name, data in hoteles.items():
                filtered_opiniones = [op for op in data['opiniones'] if keyword in op.get('cluster_keywords', [])]
                if filtered_opiniones:
                    filtered_hoteles[hotel_name] = {
                        'direccion': data['direccion'],
                        'opiniones': filtered_opiniones
                    }
            hoteles = filtered_hoteles

        return render(request, 'turismo/hoteles.html', {'hoteles': hoteles,
                                                        'unique_keywords': unique_keywords,
                                                        'keyword': keyword,
                                                        'municipios': municipios})

    return render(request, 'turismo/hoteles.html', {'municipios': municipios})
