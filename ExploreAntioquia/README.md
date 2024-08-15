# ExploreAntioquia

ExploreAntioquia es una aplicación sencilla de Django. 
Este repositorio proporciona instrucciones sobre cómo ejecutar la aplicación localmente usando Docker.

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalados en tu máquina local:

- [Docker](https://www.docker.com/get-started)

## Ejecutar la Aplicación Localmente

1. **Descargar la Imagen Docker desde Docker Hub**

   Primero, descarga la imagen Docker desde Docker Hub. Esta imagen contiene la aplicación preconstruida:

   ```bash
   docker pull juanqu/explore-antioquia:1.1
   ```
2. **Configurar el Archivo .env**

   Para que la aplicación funcione correctamente, hay configurar el archivo .env
   El archivo debe estar en la raíz del directorio del proyecto y debe incluir las credenciales para la base de datos.
   Esta base de datos puede ser local, en cualquier caso la app usa POSTGRESQL.

   **Ejemplo de archivo .env**
   
   DB_NAME=tu_nombre_de_base_de_datos
   
   DB_USER=tu_usuario_de_base_de_datos
   
   DB_PASSWORD=tu_contraseña_de_base_de_datos
   
   DB_HOST=db
   
   DB_PORT=5432

4. **Ejecutar el contenedor**

   ```bash
   docker run -p 8000:8000 --env-file .env juanqu/explore-antioquia:1.1
   ```

   Asi se puede correr la imagen cargando tus crendenciales.

5. **Aplicar Migraciones y Crear Superusuario**

   Una vez que el contenedor esté en ejecución, deberás aplicar las migraciones para configurar la base de datos y crear un superusuario para acceder al panel de administración de Django.

   **Activar la nueva base de datos**
   
   ```bash
   docker exec -it <container_id> python manage.py migrate
   ```

   Reemplaza <container_id> con el id del contenedor que se haya ejecutado (se puede ver con: docker ps).

   **Crear superusurio**

   ```bash
   docker exec -it <container_id> python manage.py createsuperuser
   ```
   Sigue las instrucciones de la terminal.

6. **Acceder a la app**

   Con estas configuraciones, la app deberia estar alojada en: http://localhost:8000
   
