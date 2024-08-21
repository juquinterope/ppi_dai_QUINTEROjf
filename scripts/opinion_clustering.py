from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore
from sklearn.cluster import KMeans  # type: ignore
from hoteles import obtener_hoteles_cercanos, reviews
from nltk.corpus import stopwords  # type: ignore
import numpy as np
# from collections import Counter


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
    all_reviews = [review['text']
                   for hotel in hotels_data for review in hotel['reviews']]

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
    clusters_keywords = extract_top_keywords_per_cluster(
        X, clusters, feature_names)

    # Asignación de clústeres y palabras clave a las opiniones originales
    index = 0
    for hotel in hotels_data:
        for review in hotel['reviews']:
            review['cluster'] = clusters[index]
            review['cluster_keywords'] = clusters_keywords[clusters[index]]
            index += 1

    return hotels_data


# Ejemplo de uso

if __name__ == '__main__':
    # Ejemplo de uso
    latitud = 6.2442   # Latitud de Medellín, Antioquia
    longitud = -75.5812  # Longitud de Medellín, Antioquia
    hoteles = obtener_hoteles_cercanos(latitud, longitud, 'MEDELLIN')
    # print(hoteles)
    opiniones = []
    for hotel in hoteles[:3]:
        review = reviews(hotel['id'], hotel['nombre'], hotel['direccion'])
        opiniones.append(review)

    cluster = cluster_opinions_by_hotel(opiniones)
    print(cluster)
