FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema (si se necesitan)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar y instalar dependencias Python
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Exponer puerto (Flask por defecto)
EXPOSE 5000

# Comando para iniciar la app
CMD ["python", "app.py"]
