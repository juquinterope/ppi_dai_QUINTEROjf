import time
import pandas as pd
import geopandas as gpd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Configurar Selenium
# chrome_options = Options()
# chrome_options.add_argument("--headless")  # Ejecutar Chrome en segundo plano

driver = webdriver.Chrome()

# Cargar el GeoDataFrame
gdf = gpd.read_file('../ExploreAntioquia/data/municipios_antioquia.geojson')

# Función para formatear el nombre
def format_name(name):
    parts = name.split()
    formatted = '_'.join([part.capitalize() for part in parts])
    return formatted

# Crear una nueva columna 'Descripcion' en el GeoDataFrame
gdf['Descripcion'] = ""

for index, row in gdf.iterrows():
    municipio = row['Nombre Municipio']
    formatted_name = format_name(municipio)
    url = f'https://es.wikipedia.org/wiki/{formatted_name}'
    
    driver.get(url)
    time.sleep(2)  # Esperar 2 segundos

    try:
        # Encontrar el primer <p> después de un <h2> con id=Historia
        historia_element = driver.find_element(By.ID, 'Historia')
        p_element = historia_element.find_element(By.XPATH, 'following-sibling::p')
        descripcion = p_element.text
    except Exception as e:
        descripcion = "No se encontró descripción"
        print(f"Error al buscar {formatted_name}: {e}")

    # Actualizar el GeoDataFrame con la descripción obtenida
    gdf.at[index, 'Descripcion'] = descripcion

# Guardar el GeoDataFrame actualizado
gdf.to_file('../ExploreAntioquia/data/municipios_antioquia_actualizado.geojson', driver='GeoJSON')

driver.quit()
