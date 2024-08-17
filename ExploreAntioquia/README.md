# ExploreAntioquia

ExploreAntioquia es una aplicación sencilla de Django. 
Este repositorio proporciona instrucciones sobre cómo ejecutar la aplicación localmente usando Docker.

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalados en tu máquina local:

- [Docker](https://www.docker.com/get-started)
- Crear un directorio y abrir una nueva terminal dentro de este.

## Ejecutar la Aplicación Localmente

1. **Crear la Imagen Docker a partir de Docker Hub**

   Primero, descarga la imagen Docker desde Docker Hub dentro de un directorio. Esta imagen contiene la aplicación preconstruida:

   ```bash
   docker pull juanqu/explore-antioquia:1.3
   ```

   Crear un contenedor temporal para acceder a los archivos:
   ```bash
   docker create --name temp-container explore-antioquia:1.3
   ```
   Copiar el archivo entrypoint.sh del contenedor temporal a la máquina local:
   ```bash
   docker cp temp-container:/app/entrypoint.sh ./entrypoint.sh
   ```
   Detener y remover el contenedor temporal:
   ```bash
   docker rm temp-container
   ```

   Modifica el archivo entrypoint.sh que se creo en el directorio local.
   'entrypoint.sh file'
   ```bash
   #!/bin/bash
   set -e

   # Migrar nueva base de datos
   echo "Exportando esquema de la base de datos..."
   python manage.py makemigrations
   python manage.py migrate
   
   # Ejecutar collectstatic
   echo "Running collectstatic..."
   python manage.py collectstatic --noinput
   
   # Iniciar Gunicorn
   echo "Starting Gunicorn..."
   exec gunicorn --bind 0.0.0.0:8000 ExploreAntioquia.wsgi:application
   ```
   
   Una vez que hayas modificado entrypoint.sh, puedes crear un nuevo Dockerfile que use la imagen original como base e incluya el entrypoint.sh modificado:
   ```bash
   echo -e "FROM explore-antioquia:1.2\nCOPY entrypoint.sh /app/entrypoint.sh\nENTRYPOINT [\"/bin/sh\", \"/app/entrypoint.sh\"]" > Dockerfile
   ```
   Construir una nueva imagen con el entrypoint.sh modificado:
   ```bash
   docker build -t explore-antioquia-modificada .
   ```
3. **Configurar el Archivo .env**

   Para que la aplicación funcione correctamente, hay configurar el archivo .env
   El archivo debe estar en la raíz del directorio del proyecto y debe incluir las credenciales requeridas.
   La base de datos puede ser local, en cualquier caso debe usar el motor PostgreSQL.

   **Ejemplo de archivo .env**
   
   DB_NAME=tu_nombre_de_base_de_datos
   
   DB_USER=tu_usuario_de_base_de_datos
   
   DB_PASSWORD=tu_contraseña_de_base_de_datos
   
   DB_HOST=db
   
   DB_PORT=5432

   WEATHER_API=openweathermap_api

   PLACES_API=tu_api_places_de_google

5. **Ejecutar el contenedor**

   ```bash
   docker run -p 8000:8000 --env-file .env explore-antioquia-modificada
   ```

   Asi se puede correr la imagen cargando tus crendenciales.

6. **Acceder a la app**

   Con estas configuraciones, la app deberia estar alojada en: http://localhost:8000
   
