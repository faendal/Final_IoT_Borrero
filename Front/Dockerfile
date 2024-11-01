# Usar una imagen base de Python
FROM python:3.11.5-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo de dependencias primero para aprovechar la caché
COPY requirements.txt /app/requirements.txt

# Instalar las dependencias desde requirements.txt
RUN pip install -r /app/requirements.txt

# Copiar el resto de la aplicación al contenedor
COPY . /app

# Exponer el puerto de la aplicación en el contenedor
EXPOSE 80

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]