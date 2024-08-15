import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from mpl_toolkits.axes_grid1 import make_axes_locatable
import contextily as ctx  # type: ignore


def mapa_calor(gdf):
    """
    Genera un mapa de calor para un GeoDataFrame utilizando datos de temperatura.

    Esta función crea un mapa visualizando las coordenadas geográficas contenidas en el GeoDataFrame `gdf`,
    aplica un mapa de calor basado en las temperaturas y añade un mapa base utilizando `contextily`.

    Parámetros:
    -----------
    gdf : GeoDataFrame
        Un GeoDataFrame que contiene las coordenadas geográficas y una columna de temperatura.
        Se espera que `gdf` tenga una columna llamada 'geometry' con las geometrías y una columna 'temperatura'
        con los valores de temperatura que se utilizarán para el mapa de calor.

    Ejemplos:
    ---------
    >>> import geopandas as gpd
    >>> import pandas as pd
    >>> from shapely.geometry import Point
    >>>
    >>> # Crear un DataFrame con datos de ejemplo
    >>> df = pd.DataFrame({
    >>>     'lat': [4.56, 4.60],
    >>>     'lon': [-74.05, -74.01],
    >>>     'temperatura': [22, 30]
    >>> })
    >>> df['geometry'] = df.apply(lambda x: Point(x['lon'], x['lat']), axis=1)
    >>> gdf = gpd.GeoDataFrame(df, geometry='geometry', crs='EPSG:4326')
    >>>
    >>> mapa_calor(gdf)

    Notas:
    ------
    - La columna 'temperatura' debe contener los valores numéricos que se usarán para el mapa de calor.
    - La función utiliza el CRS 'EPSG:3857' para el mapa base. Asegúrate de que el GeoDataFrame esté en este CRS.
    - El mapa base es proporcionado por `contextily` y se utiliza el proveedor `CartoDB.Positron`.

    Requisitos:
    ------------
    - geopandas
    - matplotlib
    - contextily
    - mpl_toolkits.axes_grid1

    """
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

    # Usar ScalarMappable solo una vez para la barra de color
    sm = plt.cm.ScalarMappable(cmap='coolwarm', norm=Normalize(
        vmin=gdf['temperatura'].min(), vmax=gdf['temperatura'].max()))
    sm.set_array([])  # No necesita datos, solo el cmap y norm

    # Añadir la barra de color
    cbar = fig.colorbar(sm, cax=cax)
    cbar.set_label('Temperatura')

    ax.set_title('Mapa de Temperaturas en Municipios')
    plt.show()
