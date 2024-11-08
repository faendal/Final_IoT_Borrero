# Sistema de monitoreo a planta suculenta

Este proyecto es un sistema de monitoreo para una planta suculenta que mide la temperatura y la humedad del aire y de la tierra. El sistema está compuesto por varios componentes que se describen a continuación.

El proyecto está pensado para ser ejecutado en un ubuntu 22.04 en EC2 de AWS.

## Estructura del Proyecto

### Backend

El backend del proyecto se configura utilizando Docker Compose. Aquí se definen los servicios necesarios para la base de datos y la visualización de datos.

- **docker-compose.yml**: Archivo de configuración de Docker Compose que define los servicios de MongoDB, CrateDB, Orion, QuantumLeap y Grafana. Adicionalmente, se incluye la imagen creada manualmente para correr el frontend de la aplicación.

### Front

El frontend del proyecto está desarrollado en Python utilizando Dash para la visualización de datos.

- **app.py**: Archivo principal de la aplicación Dash que define el layout y los callbacks para la visualización de datos.
- **Dockerfile**: Archivo de configuración de Docker para construir la imagen de la aplicación.
- **requirements.txt**: Archivo que lista las dependencias de Python necesarias para la aplicación.

### Imagenes

Esta carpeta contiene imágenes de la planta suculenta que se utilizan en la aplicación frontend.

### Sensores

Esta carpeta contiene el código y la configuración para los sensores que miden la temperatura y la humedad.

- **.gitignore**: Archivo de configuración para ignorar archivos específicos en Git.
- **.pio/**: Carpeta generada por PlatformIO que contiene los archivos de construcción y dependencias.
- **.vscode/**: Carpeta de configuración para Visual Studio Code.
- **include/**: Carpeta destinada a archivos de cabecera del proyecto.
- **lib/**: Carpeta destinada a bibliotecas del proyecto.
- **platformio.ini**: Archivo de configuración de PlatformIO para el proyecto.
- **src/**: Carpeta que contiene el código fuente del proyecto.
- **test/**: Carpeta destinada a pruebas del proyecto.

## Cómo ejecutar el proyecto

### Backend y Frontend

Para poder correr el proyecto se debe tener instalado Docker, Docker Compose y Python.

Se debe asegurar de tener los archivos `docker-compose.yml` en el directorio inicial y `app.py`, `Dockerfile` y `requirements.txt` en el directorio `app` del entorno de ejecución que se va a utilizar.

Para ejecutar el proyecto, ejecuta los siguientes comandos:

```sh
sudo systemctl max_map_count=262144
```


```sh
sudo docker-compose up --build -d
```

De esta manera, los servicios requeridos por la aplicación se levantarán en contenedores de Docker.

### Sensores

Para poder correr el proyecto se debe tener instalado PlatformIO. Se debe asegurar de tener los archivos `platformio.ini` en el directorio inicial y el código fuente en la carpeta `src`. Se debe compilar el código, subirlo al microcontrolador y ejecutarlo a través del monitor serial. Esto enviará los datos al servidor de Orion, el cual los almacenará en la base de datos CrateDB.
