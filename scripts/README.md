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
