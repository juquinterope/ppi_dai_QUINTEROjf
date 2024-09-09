import base64
from io import BytesIO
from decouple import config  # type: ignore
import contextily as ctx  # type: ignore
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import Normalize
import matplotlib.pyplot as plt
import geopandas as gpd  # type: ignore
import requests
import matplotlib
# Usar backend 'Agg' para evitar GUI warnings
matplotlib.use('Agg')


def municipios_mas_cercanos(nombre_municipio, municipios, num_cercanos=5):
    """Encuentra los municipios más cercanos a un municipio de referencia 
    utilizando geometría geoespacial.

    Esta función selecciona un municipio de referencia por su nombre, 
    calcula la distancia a todos los demás municipios, y devuelve una 
    lista de los municipios más cercanos junto con su distancia en metros 
    y sus coordenadas.

    Args:
        nombre_municipio (str): El nombre del municipio de referencia.
        municipios (GeoDataFrame): Un GeoDataFrame que contiene la geometría 
                                   y los datos de los municipios.
        num_cercanos (int, opcional): El número de municipios más cercanos 
                                      a devolver. El valor predeterminado 
                                      es 5.

    Returns:
        GeoDataFrame: Un GeoDataFrame con los municipios más cercanos, 
                      incluyendo el nombre, la distancia, la latitud 
                      y la longitud. Devuelve `None` si el municipio 
                      de referencia no se encuentra.
    """
    # Seleccionar el municipio de referencia
    municipio_ref = municipios[municipios['Nombre Municipio']
                               == nombre_municipio]

    if municipio_ref.empty:
        print(
            f"El municipio {nombre_municipio} no fue encontrado en el archivo GeoJSON.")
        return None

    # Obtener la geometría del municipio de referencia
    geom_ref = municipio_ref.geometry.iloc[0]

    # Calcular la distancia de todos los municipios al municipio de referencia
    municipios['distancia'] = municipios.geometry.distance(geom_ref)

    # Ordenar los municipios por distancia y seleccionar los más cercanos
    municipios_cercanos = municipios.sort_values(
        'distancia').head(num_cercanos)

    # Devuelve la distancia en metros
    return municipios_cercanos[['Nombre Municipio', 'distancia', 'Latitud', 'Longitud']]


def obtener_datos_climaticos(lat, lon):
    """Obtiene datos climáticos actuales para una ubicación específica 
    utilizando la API de OpenWeatherMap.

    Esta función realiza una solicitud a la API de OpenWeatherMap para 
    obtener la temperatura actual y una descripción del clima para 
    las coordenadas proporcionadas. 

    Args:
        lat (float): Latitud de la ubicación deseada.
        lon (float): Longitud de la ubicación deseada.

    Returns:
        dict: Un diccionario con la temperatura actual ('temperatura') 
              y la descripción del clima ('descripcion') en español si 
              la solicitud es exitosa.
        None: Devuelve `None` si la solicitud a la API falla.
    """

    api_key = config('WEATHER_API')

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


def mapa_calor(gdf):
    """Genera un mapa de calor de temperaturas basado en un GeoDataFrame, 
    y lo convierte en una imagen codificada en base64.

    La función crea un mapa de calor sobre un mapa base que muestra las 
    temperaturas en diferentes municipios. También genera una tabla 
    con los nombres de los municipios y sus temperaturas correspondientes.
    La imagen resultante se guarda en un objeto BytesIO y se convierte 
    a una cadena base64 para ser utilizada en aplicaciones web.

    Args:
        gdf (GeoDataFrame): Un GeoDataFrame que contiene la geometría y 
                            los datos de temperatura de los municipios.

    Returns:
        str: Una cadena de texto que representa la imagen del mapa de calor 
             codificada en formato base64.
    """
    # Crear la figura y los ejes
    fig, ax = plt.subplots(1, 2, figsize=(
        16, 8), gridspec_kw={'width_ratios': [4, 1]})

    # Graficar el mapa base con el mapa de calor en el primer eje
    gdf.plot(ax=ax[0], alpha=0.6, edgecolor='k', cmap='coolwarm', legend=False,
             markersize=100, column='temperatura', norm=Normalize(vmin=gdf['temperatura'].min(), vmax=gdf['temperatura'].max()))

    # Añadir el mapa base
    ctx.add_basemap(ax[0], crs=gdf.crs.to_string(),
                    source=ctx.providers.CartoDB.Positron)

    # Eliminar las etiquetas de los ejes (x, y)
    ax[0].set_xticks([])
    ax[0].set_yticks([])

    # Ajustar la leyenda del mapa de calor
    divider = make_axes_locatable(ax[0])
    cax = divider.append_axes("right", size="5%", pad=0.1)

    # Usar ScalarMappable para la barra de color
    sm = plt.cm.ScalarMappable(cmap='coolwarm', norm=Normalize(
        vmin=gdf['temperatura'].min(), vmax=gdf['temperatura'].max()))
    # Pasar los datos de temperatura al ScalarMappable
    sm.set_array(gdf['temperatura'])

    # Añadir la barra de color
    cbar = fig.colorbar(sm, cax=cax)
    cbar.set_label('Temperatura')

    ax[0].set_title('Mapa de Temperaturas en Municipios cercanos')

    # Crear la tabla en el segundo eje
    table_data = list(zip(gdf['Nombre Municipio'], gdf['temperatura']))
    table = ax[1].table(cellText=table_data, colLabels=['Municipio', 'Temperatura'], loc='center',
                        colWidths=[1.1, 0.4])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)  # Ajustar tamaño de la tabla

    # Quitar los ejes del gráfico de la tabla
    ax[1].axis('off')

    # Guardar la imagen en un objeto de BytesIO
    buffer = BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight')
    plt.close(fig)  # Cerrar la figura para liberar memoria

    # Convertir la imagen a base64
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    return image_base64
