import requests
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer # type: ignore
from sklearn.cluster import KMeans # type: ignore
from nltk.corpus import stopwords # type: ignore
from decouple import config # type: ignore

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
    api_key = config('TRIPADVISOR_API')
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


def reviews(id, nombre, direccion):
    """
    Obtiene reseñas de un lugar específico de TripAdvisor usando su API.

    Args:
        id (str): El identificador del lugar en TripAdvisor para el cual se desean obtener las reseñas.

    Returns:
        list: Una lista que contiene:
            - Un array de NumPy en la posicion 0 con los ratings de las reseñas.
            - Un array de NumPy en la posicion 1 con el número de votos útiles de las reseñas.
            - Una lista de diccionarios, cada uno representando una reseña sin el rating, que incluye:
                - 'text': El texto de la reseña.
                - 'date': La fecha del viaje.
                - 'trip': El tipo de viaje.

    Raises:
        ValueError: Si la respuesta de la API no tiene el formato esperado o si ocurre un error en la solicitud.
    """
    api_key = config('TRIPADVISOR_API')
    review_url = f'https://api.content.tripadvisor.com/api/v1/location/'
    params = {
        'key': api_key,
        'language': 'es_CO',
        # Número máximo de reseñas a recuperar
        'limit': 10
    }

    # Realiza una solicitud GET a la API para obtener reseñas para el lugar con el id proporcionado
    response_2 = requests.get(review_url + f'{id}/reviews', params=params)

    # Verifica si la solicitud fue exitosa (código de estado 200)
    if response_2.status_code == 200:
        # Convierte la respuesta JSON a un diccionario de Python y obtiene la lista de reseñas
        data = response_2.json().get('data', [])

        # Inicializa listas para almacenar ratings y reseñas
        reviews = []
        ratings = []

        # Itera sobre cada reseña en los datos obtenidos
        for review in data:
            # Agrega el rating de la reseña a la lista de ratings
            ratings.append(review['rating'])

            # Agrega un diccionario con el texto, la fecha de viaje y el tipo de viaje a la lista de reseñas
            reviews.append({
                'text': review['text'],  # Texto de la reseña
                'date': review['travel_date'],  # Fecha del viaje
                'trip': review['trip_type']  # Tipo de viaje
            })
        
        # Convierte las listas de ratings y votos a arrays de NumPy
        # ratings = np.array(ratings)

    else:
        # Manejo de errores si la solicitud no es exitosa
        raise ValueError(f'Error en la solicitud: {response_2.status_code}')
    
    # Retorna una lista con el array de ratings, el array de votos y luego las reseñas
    return {'nombre': nombre, 'direccion': direccion, 'ratings': ratings, 'reviews': reviews}


def extract_top_keywords_per_cluster(tfidf_matrix, cluster_labels, feature_names, top_n=5):
    clusters_keywords = {}
    for cluster in np.unique(cluster_labels):
        # Filtrar las filas pertenecientes al clúster actual
        cluster_indices = np.where(cluster_labels == cluster)
        cluster_data = tfidf_matrix[cluster_indices]

        # Sumar las frecuencias de palabras en el clúster
        word_frequencies = np.sum(cluster_data, axis=0)

        # Extraer los índices de las palabras con mayor frecuencia
        top_word_indices = np.argsort(word_frequencies)[0, -top_n:]

        # Obtener las palabras correspondientes
        top_keywords = [feature_names[i] for i in top_word_indices]
        clusters_keywords[cluster] = top_keywords

    return clusters_keywords

def cluster_opinions_by_hotel(hotels_data, n_clusters=5):
    """
    Agrupa opiniones por temas para cada hotel utilizando KMeans.

    :param hotels_data: Lista de diccionarios, cada uno representando un hotel con sus opiniones.
    :param n_clusters: Número de clusters/temas a identificar por hotel.
    :return: Lista de hoteles, cada uno con sus opiniones agrupadas por temas.
    """

    # Extraer todas las opiniones
    all_reviews = [review['text'] for hotel in hotels_data for review in hotel['reviews']]

    # Cargar stop words en español de nltk
    spanish_stop_words = stopwords.words('spanish')

    # Vectorización de las opiniones
    vectorizer = TfidfVectorizer(stop_words=spanish_stop_words)
    X = vectorizer.fit_transform(all_reviews)

    # Aplicación de KMeans clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    clusters = kmeans.fit_predict(X)

    # Extraer palabras clave representativas de cada clúster
    feature_names = vectorizer.get_feature_names_out()
    clusters_keywords = extract_top_keywords_per_cluster(X, clusters, feature_names)

    # Asignación de clústeres y palabras clave a las opiniones originales
    index = 0
    for hotel in hotels_data:
        for review in hotel['reviews']:
            review['cluster'] = int(clusters[index])
            review['cluster_keywords'] = clusters_keywords[clusters[index]][0].flatten().tolist()
            index += 1

    return hotels_data
