FROM python:3.10-slim

# Instalar ping
RUN apt-get update && apt-get install -y iputils-ping && apt-get clean

WORKDIR /app

# Instala streamlit y cualquier otra dependencia
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de archivos
COPY . .

# Expone el puerto que usa Streamlit
EXPOSE 8501

# Arranca la app automáticamente
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
