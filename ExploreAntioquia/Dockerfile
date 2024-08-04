# Imagen base de Python
FROM python:3.11

WORKDIR /app

# Copia los archivos del proyecto
COPY . /app

# Instala las dependencias del sistema
RUN apt-get update && \
    apt-get install -y \
    pkg-config \
    libffi-dev \
    libgeos-dev \
    libgdal-dev

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Comando para ejecutar la aplicación
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ExploreAntioquia.wsgi:application"]
