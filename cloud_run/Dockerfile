FROM python:3.11-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos necesarios al directorio de trabajo
COPY main.py .
COPY requirements.txt .
COPY templates/ templates/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "main.py"]