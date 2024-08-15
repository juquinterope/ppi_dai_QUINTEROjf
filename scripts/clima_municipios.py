import geopandas as gpd  # type: ignore
import requests
import pandas as pd


# Leer el archivo GeoJSON
geojson_file = "../ExploreAntioquia/data/municipios_antioquia_actualizado.geojson"
municipios = gpd.read_file(geojson_file)


def obtener_datos_climaticos(lat, lon):
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
