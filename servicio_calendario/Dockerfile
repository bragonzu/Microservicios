# Usamos una imagen de Python como base
FROM python:3.9-slim

# Establecemos el directorio de trabajo en /app
WORKDIR /app

# Copiamos el archivo de requisitos y lo instalamos
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copiamos el código de la aplicación al contenedor
COPY . .

# Exponemos el puerto 5000
EXPOSE 5000

# Comando para ejecutar la aplicación Flask
CMD ["python", "app.py"]
