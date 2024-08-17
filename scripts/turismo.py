import requests
from typing import List, Dict, Any


def search_places(api_key: str, latitude: float, longitude: float, place_type: str, radius: int = 3000) -> List[Dict[str, Any]]:
    """
    Busca lugares cercanos a las coordenadas especificadas usando la API de Places de Google.

    Parámetros:
    - api_key (str): Tu clave de API de Google.
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
        'key': api_key,
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

        return sorted_results
    else:
        print(f"Error en la solicitud: {response.status_code}")
        return []


# Ejemplo de uso
if __name__ == "__main__":
    API_KEY = 'api_key'
    LATITUDE = 6.2518
    LONGITUDE = -75.5636
    # Cambiar a 'lodging' para hoteles
    PLACE_TYPE = 'restaurant'

    places = search_places(API_KEY, LATITUDE, LONGITUDE, PLACE_TYPE)

    for place in places:
        name = place.get('name', 'No disponible')
        address = place.get('vicinity', 'No disponible')
        rating = place.get('rating', 'No disponible')
        print(f"Nombre: {name}")
        print(f"Dirección: {address}")
        print(f"Rating: {rating}")
        print("------")
