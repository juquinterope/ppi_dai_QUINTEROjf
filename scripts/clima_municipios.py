import geopandas as gpd  # type: ignore
import requests
import pandas as pd


# Leer el archivo GeoJSON
geojson_file = "../ExploreAntioquia/data/municipios_antioquia_actualizado.geojson"
municipios = gpd.read_file(geojson_file)


def obtener_datos_climaticos(lat, lon):
    """Esta función realiza una solicitud a la API de OpenWeatherMap para obtener
    los datos climáticos actuales de una ubicación específica basada en su
    latitud y longitud. Retorna la temperatura y una descripción del clima en el idioma español.

    Parámetros:

    lat (float): La latitud de la ubicación para la cual se desea obtener los datos climáticos.
    lon (float): La longitud de la ubicación para la cual se desea obtener los datos climáticos.

    Retorno:

    dict: Un diccionario que contiene dos claves:
    'temperatura': Un valor float que representa la temperatura actual en grados Celsius.
    'descripcion': Un string que describe las condiciones climáticas actuales en español.
    Si la solicitud a la API falla (status code diferente de 200), la función retorna None.

    -----------------------------------------------------------------------------------------------
    Consideraciones:
    Es necesario contar con una clave API válida de OpenWeatherMap para que la función funcione correctamente.
    La unidad de temperatura devuelta es en grados Celsius, y la descripción del clima está en español.
    La URL de la solicitud excluye datos minuciosos, horarios, diarios y alertas para enfocarse solo en las condiciones actuales.
    """
    api_key = "tu_api"

    base_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,daily,alerts&appid={api_key}&units=metric&lang=es"
    response = requests.get(base_url)
    if response.status_code == 200:
        data = response.json()
        return {
            'temperatura': data['current']['temp'],
            'descripcion': data['current']['weather'][0]['description']
        }
    else:
        return None


# Seleccionar un solo municipio por su nombre
nombre_municipio = "MEDELLÍN"
municipio = municipios[municipios['Nombre Municipio'] == nombre_municipio]

if not municipio.empty:
    lat = municipio.iloc[0]['Latitud']
    lon = municipio.iloc[0]['Longitud']
    clima = obtener_datos_climaticos(lat, lon)
    if clima:
        datos_climaticos = {
            'municipio': nombre_municipio,
            'lat': lat,
            'lon': lon,
            **clima
        }
        # Convertir a DataFrame
        df_clima = pd.DataFrame([datos_climaticos])
        print(df_clima.head())
    else:
        print(
            f"No se pudo obtener la información climática para {nombre_municipio}.")
else:
    print(
        f"El municipio {nombre_municipio} no fue encontrado en el archivo GeoJSON.")
