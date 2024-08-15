import geopandas as gpd  # type: ignore


def municipios_mas_cercanos(nombre_municipio, municipios, num_cercanos=5):
    """
    Encuentra los municipios más cercanos a un municipio de referencia en un GeoDataFrame.

    Esta función busca los municipios más cercanos al municipio especificado en el GeoDataFrame `municipios`.
    Utiliza la distancia geográfica para determinar qué municipios están más cerca del municipio de referencia.

    Parámetros:
    -----------
    nombre_municipio : str
        El nombre del municipio de referencia para encontrar los municipios más cercanos.

    municipios : GeoDataFrame
        Un GeoDataFrame que contiene la información de los municipios, incluyendo columnas de geometría y nombre del municipio.
        Debe tener una columna llamada 'Nombre Municipio' con el nombre de los municipios y columnas 'Latitud' y 'Longitud' con sus coordenadas.

    num_cercanos : int, opcional, default=5
        El número de municipios más cercanos a devolver. Por defecto es 5.

    Retorna:
    --------
    DataFrame
        Un DataFrame con los municipios más cercanos, que incluye las siguientes columnas:
        - 'Nombre Municipio': Nombre del municipio cercano.
        - 'distancia': Distancia al municipio de referencia en metros.
        - 'Latitud': Latitud del municipio cercano.
        - 'Longitud': Longitud del municipio cercano.

    Ejemplos:
    ---------
    >>> import geopandas as gpd
    >>> geojson_file = "../ExploreAntioquia/data/municipios_antioquia_actualizado.geojson"
    >>> municipios = gpd.read_file(geojson_file)
    >>> municipios = municipios.to_crs(epsg=3116)
    >>> resultados = municipios_mas_cercanos("Medellín", municipios)
    >>> print(resultados)

    Notas:
    ------
    - La función asume que el GeoDataFrame `municipios` ya está proyectado en un sistema de coordenadas adecuado (e.g., UTM).
    - La columna 'Nombre Municipio' debe existir en el GeoDataFrame `municipios` para identificar el municipio de referencia.
    - La función calcula la distancia en metros usando la geometría del municipio de referencia.
    - Si el municipio de referencia no se encuentra en el GeoDataFrame, la función devuelve `None`.

    Requisitos:
    ------------
    - geopandas
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
    municipios_cercanos = municipios.sort_values('distancia').head(num_cercanos)

    # Devuelve la distancia en metros
    return municipios_cercanos[['Nombre Municipio', 'distancia', 'Latitud', 'Longitud']]
