import requests
from typing import List, Dict, Any
from decouple import config  # type: ignore


def search_places(latitude: float, longitude: float, place_type: str, radius: int = 3000) -> List[Dict[str, Any]]:
    """
    Busca lugares cercanos a las coordenadas especificadas usando la API de Places de Google.

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

        # Filtrar y ordenar por rating
        sorted_results = sorted(
            results, key=lambda x: x.get('rating', 0), reverse=True)
        results = []
        for place in sorted_results:
            name = place.get('name', 'No disponible')
            address = place.get('vicinity', 'No disponible')
            rating = place.get('rating', 'No disponible')
            place_id = place.get('place_id', 'No disponible')
            results.append(
                {'nombre': name, 'direccion': address, 'rating': rating, 'place_id': place_id})
        return results
    else:
        # print(f"Error en la solicitud: {response.status_code}")
        return 'fallo'
