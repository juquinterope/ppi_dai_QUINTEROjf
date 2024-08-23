# scripts
El dataframe original con informacion sobre los municipios se obtuvo de [Geoportal del Dane](https://geoportal.dane.gov.co/geovisores/territorio/consulta-divipola-division-politico-administrativa-de-colombia/)

### 1. Limpieza
<limpiar_municipios.py> Es un script sencillo que filtra los datos relevantes sobre los mmunicipios.

### 2. Creacion de coordenadas
<puntos_geometricos.py> Toma la informacion filtrada y lleva los municipios a coordenadas usando [geopandas](https://geopandas.org/en/stable/)

### 3. Obtener descripciones
<descripcion_municipios.py> Implementa un driver de chrome usando [selenium](https://selenium-python.readthedocs.io/) para buscar informacion sobre todos los municipios.

### Datos en ExploreAntioquia
Luego de pasar por todos los scripts, ese geojson final son los datos cargados por al app.

### 4. Recolectar clima en tiempo real
<clima_municipios.py> Implementa el llamado a la api de [OpenWeatherMap](https://openweathermap.org/api) para recolectar el clima en tiempo real de un municipio dado.

### 5. Buscar municipios cercanos
<municipios_cercanos.py> Busca los municipios mas cercanos al municipio de interes, teniendo en cuenta el geodataframe sobre los [municipios de Antioquia](https://github.com/juquinterope/ppi_dai_QUINTEROjf/blob/main/ExploreAntioquia/data/municipios_antioquia_actualizado.geojson) de la app.

### 6. Mapa de temperaturas
<mapa_temperaturas.py> Sobre un mapa base de [contextily](https://contextily.readthedocs.io/en/latest/) aplica un mapa de calor sobre temperaturas de los puntos geograficos dados.

### 7. Places API de Google
<turismo.py> Es una funcion sencilla que consulta lugares de interes de unas coordenadas dadas usando la [Places API](https://console.cloud.google.com/marketplace/product/google/places-backend.googleapis.com?q=search&referrer=search&organizationId=0) de Google, ver su documentacion para mas informacion.

### 8. Consultar opiniones de hoteles con la API de Tripadvisor
<hoteles.py> Usa la API de Tripadvisor para consultar opiniones de hoteles cercanos a una coordenada dada, devolviendo datos como: nombre, direccion, opiniones etc...

### 9. Clusterizar las opiniones
<opinion_clustering.py> Toma todas las opiniones consultadas para analizar los temas principales de estos y agrupar las opiniones segun esos temas, usando tecnicas como: Kmeans y TF-IDF.
