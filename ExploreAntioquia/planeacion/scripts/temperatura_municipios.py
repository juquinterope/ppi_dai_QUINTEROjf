import geopandas as gpd  # type: ignore
import requests
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from mpl_toolkits.axes_grid1 import make_axes_locatable
import contextily as ctx  # type: ignore
from decouple import config  # type: ignore


# Leer el archivo GeoJSON
geojson_file = "../../data/municipios_antioquia_actualizado.geojson"
municipios = gpd.read_file(geojson_file)

# Reproyectar a un sistema de coordenadas proyectado (UTM, por ejemplo EPSG:3116 para Colombia)
municipios = municipios.to_crs(epsg=3116)


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

    # Ordenar los municipios por distancia y seleccionar los más cercanos (excluyendo el propio municipio)
    municipios_cercanos = municipios[municipios['Nombre Municipio']
                                     != nombre_municipio].sort_values('distancia').head(num_cercanos)

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


# Ejemplo de uso
# Cambia esto por el nombre del municipio que deseas consultar
nombre_municipio = "ANZÁ"
municipios_cercanos = municipios_mas_cercanos(nombre_municipio, municipios)
municipios_cercanos['temperatura'] = municipios_cercanos.apply(
    lambda x: obtener_datos_climaticos(
        x['Latitud'], x['Longitud'])['temperatura'],
    axis=1)

if municipios_cercanos is not None:
    print(municipios_cercanos)

gdf = gpd.GeoDataFrame(
    municipios_cercanos,
    geometry=gpd.points_from_xy(
        municipios_cercanos.Longitud, municipios_cercanos.Latitud)
)

# Asignar el CRS inicial (WGS 84)
# EPSG:4326 es para coordenadas geográficas (lat/lon)
gdf = gdf.set_crs(epsg=4326)

# Reproyectar a un CRS métrico adecuado
gdf = gdf.to_crs(epsg=3116)  # EPSG:3116 es un CRS métrico para Colombia


def mapa_calor(gdf):
    # Crear el mapa
    # Crear la figura y los ejes
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))

    # Graficar el mapa base
    gdf.plot(ax=ax, alpha=0.6, edgecolor='k', cmap='coolwarm', legend=False,
             markersize=100, column='temperatura', norm=Normalize(vmin=gdf['temperatura'].min(), vmax=gdf['temperatura'].max()))

    # Añadir el mapa base
    ctx.add_basemap(ax, crs=gdf.crs.to_string(),
                    source=ctx.providers.CartoDB.Positron)

    # Ajustar la leyenda del mapa de calor
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)

    # Usar ScalarMappable para la barra de color
    sm = plt.cm.ScalarMappable(cmap='coolwarm', norm=Normalize(
        vmin=gdf['temperatura'].min(), vmax=gdf['temperatura'].max()))
    sm.set_array([])  # No necesita datos, solo el cmap y norm

    # Añadir la barra de color
    cbar = fig.colorbar(sm, cax=cax)
    cbar.set_label('Temperatura')

    ax.set_title('Mapa de Temperaturas en Municipios')
    plt.show()


mapa_calor(gdf)
