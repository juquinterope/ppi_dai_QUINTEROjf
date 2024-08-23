# ExploreAntioquia

ExploreAntioquia es una aplicación sencilla de Django. 
Este repositorio proporciona instrucciones sobre cómo ejecutar la aplicación localmente.

## *Crear el entorno*

Clonar el repositorio localmente:
```bash
git clone https://github.com/juquinterope/ppi_dai_QUINTEROjf.git
```

Cambia al directorio donde esta alojado el proyecto django: /ExploreAntioquia desde el repositorio clonado:
```bash
cd ExploreAntioquia
```

Crea un entorno local de python 3.11 usando venv para correr la app:
```bash
python -m venv .venv
```
Si se cuenta con varias versiones de python, consulta como crear el entorno con esa version especifica.

Activa el entorno virtual:
```bash
.venv/Scripts/activate
```

Instala las librerias necesarias:
```bash
pip install -r requirements.txt
```

## *Configura las variables de entorno*

Recuerda estar en el directorio ./ExploreAntioquia
En la raiz del proyecto django, crea un archivo llamado: '.env' y crea estas variables:

SECRET_KEY=new_secret_key

DEBUG=True

DB_NAME=database_name

DB_USER=database_user

DB_PASSWORD=database_password

DB_HOST=database_host

DB_PORT=5432

WEATHER_API=OpenWeatherMap_API

PLACES_API=Google_places_API

TRIPADVISOR_API=tripadvisor_API


Crea una nueva secret_key para el proyecto django:
```bash
python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Copia y pega el resultado en la variable de entorno SECRET_KEY

   - ### Credenciales de la base de datos
   La aplicacion funciona con una base de datos PostgreSQL, puedes crearla localmente, al correr la app la base de datos debe estar activa.

   Puedes crear una base de datos gratuita en [render](https://dashboard.render.com/) solo se necesita crear una cuenta.

   - ### OpenWeatherMap
   Para crear una api de esta servicio dirigete a [openweathermap](https://openweathermap.org/api), crea una cuenta y luego ve a la seccion: My API keys.

   Puedes crear una API gratuita, copia la KEY de la API creada y pegala en la varible de entorno: WEATHER_API

   - ### Google maps API
   Para usar la API de maps de Google, crea una cuenta en [GCP](https://console.cloud.google.com/), puedes seguir el [tutorial](https://developers.google.com/maps/get-started) para crear al API de places.
   Cuando tengas tu API, pegala en la variable de entorno: PLACES_API

   - ### Tripadvisor API
   Crea una cuenta en [Tripadvisor](https://www.tripadvisor.com/developers) y sigue los pasos que indican para obtener la API. Esta api pegala en la variable TRIPADVISOR_API

## *Ejecutar app*

Una vez esten listas las variables de entorno, puedes correr el proyecto.

Asegurate de que los archivos estaticos estan cargados:
```bash
python manage.py collectstatic
```
Deberias ver que los archivos fueron añadidos con exito al directorio /staticfiles

Migra la app a tu base de datos:
```bash
python manage.py makemigrations
python manage.py migrate
```
Estos comandos tambien te permiten comprobar si la base de datos corre exitosamente.

Ejecuta la app:
```bash
python manage.py runserver
```

En la terminal se imprimira el link donde se estara ejecutando el proyecto.
