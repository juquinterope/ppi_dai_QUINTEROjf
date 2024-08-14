import time
import pandas as pd
import geopandas as gpd
from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()

# Cargar el GeoDataFrame
gdf = gpd.read_file('/data/municipios_antioquia.geojson')

# Función para formatear el nombre


def format_name(name):
    # Este es el unico nombre que no sigue la secuencia
    if name == "SANTA FÉ DE ANTIOQUIA":
        formatted = 'Santa_Fe_de_Antioquia'
        return formatted
    parts = name.split()
    # Capitalizar cada palabra y cambiar espacios en blanco por _
    formatted = '_'.join([part.capitalize() for part in parts])
    return formatted


# Crear una nueva columna 'Descripcion' en el GeoDataFrame
gdf['Descripcion'] = ""

# Funcion para consultar las url


def fetch_description(url):
    # Hacer que el 'bot' navegue a la url
    driver.get(url)

    # Esperar 2 segundos
    time.sleep(2)

    try:
        # Encontrar el <h2> con id=Historia
        historia_element = driver.find_element(By.ID, 'Historia')

        # Buscar el primer <p> que aparece después del <h2> con id=Historia
        p_element = historia_element.find_element(By.XPATH, 'following::p[1]')
        # Tomar el texto de la etiqueta
        descripcion = p_element.text
    except Exception as e:
        descripcion = "No se encontró descripción"
        print(f"Error al buscar {url}: {e}")

    return descripcion


# Buscaremos una url por cada municipio de Antioquia
for index, row in gdf.iterrows():
    # Tomamos unicamente el nombre
    municipio = row['Nombre Municipio']
    # Lo formateamos para la consulta en wikipedia
    formatted_name = format_name(municipio)

    # Probaremos con dos url's
    url_antioquia = f'https://es.wikipedia.org/wiki/{formatted_name}_(Antioquia)'
    url = f'https://es.wikipedia.org/wiki/{formatted_name}'

    # Intentar buscar con la URL que incluye "_(Antioquia)"
    descripcion = fetch_description(url_antioquia)

    if "No se encontró descripción" in descripcion:
        parts = formatted_name.split('_')
        formatted_name = '_'.join([part.lower() for part in parts])
        url = f'https://es.wikipedia.org/wiki/{formatted_name}'
        descripcion = fetch_description(url)

    # Si no se encuentra la etiqueta <h2> con id=Historia, buscar con la URL base
    if "No se encontró descripción" in descripcion:
        descripcion = fetch_description(url)

    # Actualizar el GeoDataFrame con la descripción obtenida
    gdf.at[index, 'Descripcion'] = descripcion

# Guardar el GeoDataFrame actualizado
gdf.to_file('../ExploreAntioquia/data/municipios_antioquia_actualizado.geojson', driver='GeoJSON')

driver.quit()
