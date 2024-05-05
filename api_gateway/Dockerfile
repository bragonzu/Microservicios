# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos de requisitos
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia los archivos de la aplicación
COPY . .

# Ejecuta la aplicación cuando se inicie el contenedor
CMD ["python", "app.py"]
