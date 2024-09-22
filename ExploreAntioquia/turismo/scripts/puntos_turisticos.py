import requests
from typing import List, Dict, Any
from decouple import config  # type: ignore


def search_places(latitude: float, longitude: float, place_type: str, words: str, radius: int = 3000) -> List[Dict[str, Any]]:
    """Busca lugares cercanos a las coordenadas especificadas usando la API de Places de Google.

    Parámetros:
    - latitude (float): Latitud del punto de búsqueda.
    - longitude (float): Longitud del punto de búsqueda.
    - place_type (str): Tipo de lugar a buscar (e.g., 'restaurant', 'lodging').
    - radius (int): Radio de búsqueda alrededor de las coordenadas en metros (default es 5000).

    Retorna:
    - List[Dict[str, Any]]: Lista de lugares cercanos, ordenada por calificación (rating) de mayor a menor.
    """
    # Endpoint de la API de Places
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

    # Parámetros de la solicitud
    params = {
        'location': f'{latitude},{longitude}',
        'radius': radius,
        'type': place_type,
        # PLACES_API (str): Tu clave de API de Google.
        'keyword': words,
        'key': config('PLACES_API'),
        'locationRestriction': {
            "circle": {
                "center": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "radius": radius
            }
        }
    }

    # Realiza la solicitud
    response = requests.get(url, params=params)

    # Verifica el estado de la solicitud
    if response.status_code == 200:
        results = response.json().get('results', [])

        # Si no se encuentran resultados, intentar con el parque principal
        if not results:
            print("No se encontraron lugares, buscando el parque principal.")
            return search_main_square(latitude, longitude, radius)

        places = []
        for place in results:
            name = place.get('name', 'No disponible')
            address = place.get('vicinity', 'No disponible')
            rating = place.get('rating', 'No disponible')
            place_id = place.get('place_id', 'No disponible')
            places.append(
                {'nombre': name, 'direccion': address, 'rating': rating, 'place_id': place_id})
        return places
    else:
        return 'Error'


def search_main_square(latitude: float, longitude: float, radius: int) -> List[Dict[str, Any]]:
    """Busca el parque principal de un municipio.

    Parámetros:
    - latitude (float): Latitud del punto de búsqueda.
    - longitude (float): Longitud del punto de búsqueda.
    - radius (int): Radio de búsqueda alrededor de las coordenadas en metros (default es 5000).

    Retorna:
    - List[Dict[str, Any]]: Parque principal del municipio 
    """

    print('Buscando parque principal')
    # Parámetros para buscar el parque principal
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    params = {
        'location': f'{latitude},{longitude}',
        'radius': radius,
        'type': 'park',  # Asumimos que el parque principal está etiquetado como 'park'
        'keyword': 'parque principal',
        'key': config('PLACES_API'),
    }

    # Realiza la solicitud
    response = requests.get(url, params=params)

    # Verifica el estado de la solicitud
    if response.status_code == 200:
        results = response.json().get('results', [])

        if results:
            # Formatear el primer resultado del parque principal
            park = results[0]
            name = park.get('name', 'Parque Principal')
            address = park.get('vicinity', 'No disponible')
            rating = park.get('rating', 'No disponible')
            place_id = park.get('place_id', 'No disponible')

            return [{'nombre': name, 'direccion': address, 'rating': rating, 'place_id': place_id}]
        else:
            # Si no se encuentra parque, devolver las coordenadas dadas
            return [{'nombre': 'Parque Principal', 'direccion': 'Coordenadas proporcionadas', 'rating': 'No disponible', 'place_id': 'No disponible'}]
    else:
        return 'Error al buscar el parque principal.'


def map_places(latitude: float, longitude: float):
    """Busca lugares de interés cerca de una ubicación dada y devuelve una lista de identificadores 
    de los lugares encontrados.

    Args:
        latitude (float): Latitud de la ubicación para buscar lugares de interés.
        longitude (float): Longitud de la ubicación para buscar lugares de interés.

    Returns:
        list of dict: Lista de diccionarios donde cada diccionario contiene un identificador 
                      de lugar ('placeId') para los lugares de interés encontrados cerca de 
                      la ubicación dada.
    """
    type = 'tourist_attraction'
    words = 'bar|park|movie_theater|art_gallery|museum|book_store|clothing_store|shopping_mall'
    places = search_places(latitude, longitude, type, words, radius=2000)
    places = [str(place['place_id']) for place in places]

    puntos = [
        {"placeId": id} for id in places
    ]

    return puntos
