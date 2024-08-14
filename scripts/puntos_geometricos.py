import geopandas as gpd
import pandas as pd
from shapely.geometry import Point


df = pd.read_csv('../ExploreAntioquia/data/municipios_filtrados.csv')
# print(df.head())

# Crear geometría de puntos a partir de las coordenadas
geometry = [Point(xy) for xy in zip(df['Longitud'], df['Latitud'])]

# Crear un GeoDataFrame
# No hay diferencias entre EPSG:4326 y WGS84
gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
gdf.to_file('../ExploreAntioquia/data/municipios_antioquia.geojson',
            driver='GeoJSON')
