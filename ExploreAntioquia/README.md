# ExploreAntioquia

ExploreAntioquia es una aplicación sencilla de Django que visualiza un mapa interactivo del departamento de Antioquia, marcando los municipios dentro de él. 
Este repositorio proporciona instrucciones sobre cómo ejecutar la aplicación localmente usando Docker.

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalados en tu máquina local:

- [Docker](https://www.docker.com/get-started)

## Ejecutar la Aplicación Localmente

1. **Descargar la Imagen Docker desde Docker Hub**

   Primero, descarga la imagen Docker desde Docker Hub. Esta imagen contiene la aplicación preconstruida:

   ```bash
   docker pull juanqu/explore-antioquia:1.0
   ```
2. **Configurar el Archivo .env**

   Para que la aplicación funcione correctamente, hay configurar el archivo .env
   El archivo debe estar en la raíz del directorio del proyecto y debe incluir las credenciales para la base de datos.
   Esta base de datos puede ser local.

   **Ejemplo de archivo .env**
   
   DB_NAME=tu_nombre_de_base_de_datos
   
   DB_USER=tu_usuario_de_base_de_datos
   
   DB_PASSWORD=tu_contraseña_de_base_de_datos
   
   DB_HOST=db
   
   DB_PORT=5432

4. **Ejecutar el contenedor**

   ```bash
   docker run -p 8000:8000 --env-file .env your_username/explore-antioquia:1.0
   ```

   Asi se puede correr la imagen cargando tus crendenciales.
