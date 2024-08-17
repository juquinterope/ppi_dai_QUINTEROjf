import requests
import numpy as np

def obtener_hoteles_cercanos(latitud, longitud, municipio):
    """
    Consulta la API de TripAdvisor para obtener hoteles cercanos a una coordenada dada.

    Parámetros:
    - latitud (float): Latitud de la ubicación.
    - longitud (float): Longitud de la ubicación.
    - municipio (str): Nombre del municipio donde se busca

    Retorna:
    - hoteles (list): Lista de diccionarios con la información de los hoteles.
    """
    # Reemplaza con tu clave API de TripAdvisor
    api_key = 'A0B5CB632FC44BE9BAEC9E29A9A6688E'
    url = "https://api.content.tripadvisor.com/api/v1/location/search"
    # headers = {"accept": "application/json"}
    params = {
        'key': api_key,
        'searchQuery': municipio,
        'category': 'hotels',
        'latLong': f'{latitud}%2C{longitud}',
        'radius': 3,
        'radiusUnit': 'km',
        'language': 'es_CO'
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        data = data.get('data', [])
        hoteles = []
        # id's de los hoteles obtenidos
        for hotel in data:
            hoteles.append({'nombre': hotel['name'], 'id': hotel.get('location_id', 'No disponible'),
                         'direccion': hotel['address_obj'].get('address_string', 'No disponible')})
            
        return hoteles
    else:
        print("Error al consultar la API:", response.status_code)
        return False

# Ejemplo de uso
# latitud = 6.2442   # Latitud de Medellín, Antioquia
# longitud = -75.5812  # Longitud de Medellín, Antioquia
# hoteles, reviews = obtener_hoteles_cercanos(latitud, longitud, 'MEDELLIN')
# print(hoteles, '\n\n', reviews)

def reviews(id):
    """
    Obtiene reseñas de un lugar específico de TripAdvisor usando su API.

    Args:
        id (str): El identificador del lugar en TripAdvisor para el cual se desean obtener las reseñas.

    Returns:
        list: Una lista que contiene:
            - Un array de NumPy con los ratings de las reseñas.
            - Un array de NumPy con el número de votos útiles de las reseñas.
            - Una lista de diccionarios, cada uno representando una reseña sin el rating, que incluye:
                - 'text': El texto de la reseña.
                - 'date': La fecha del viaje.
                - 'trip': El tipo de viaje.

    Raises:
        ValueError: Si la respuesta de la API no tiene el formato esperado o si ocurre un error en la solicitud.
    """
    api_key = 'A0B5CB632FC44BE9BAEC9E29A9A6688E'
    review_url = f'https://api.content.tripadvisor.com/api/v1/location/'
    params = {
        'key': api_key,
        'language': 'es_CO',
        # Número máximo de reseñas a recuperar
        'limit': 20
    }

    # Realiza una solicitud GET a la API para obtener reseñas para el lugar con el id proporcionado
    response_2 = requests.get(review_url + f'{id}/reviews', params=params)

    # Verifica si la solicitud fue exitosa (código de estado 200)
    if response_2.status_code == 200:
        # Convierte la respuesta JSON a un diccionario de Python y obtiene la lista de reseñas
        data = response_2.json().get('data', [])

        # Inicializa listas para almacenar ratings, votos y reseñas
        reviews = []
        ratings = []
        votes = []

        # Itera sobre cada reseña en los datos obtenidos
        for review in data:
            # Agrega el rating de la reseña a la lista de ratings
            ratings.append(review['rating'])

            # Agrega el número de votos útiles a la lista de votos
            votes.append(review['helpful_votes'])

            # Agrega un diccionario con el texto, la fecha de viaje y el tipo de viaje a la lista de reseñas
            reviews.append({
                'text': review['text'],  # Texto de la reseña
                'date': review['travel_date'],  # Fecha del viaje
                'trip': review['trip_type']  # Tipo de viaje
            })
        
        # Convierte las listas de ratings y votos a arrays de NumPy
        ratings = np.array(ratings)
        votes = np.array(votes)

    else:
        # Manejo de errores si la solicitud no es exitosa
        raise ValueError(f'Error en la solicitud: {response_2.status_code}')
    
    # Retorna una lista con el array de ratings, el array de votos y luego las reseñas
    return [ratings, votes] + reviews


opiniones = reviews(8318317)
print(opiniones)