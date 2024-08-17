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

    ax[0].set_title('Mapa de Temperaturas en Municipios')

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
