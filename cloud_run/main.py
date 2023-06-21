# API CODE
from flask import Flask, render_template, request, redirect, url_for
from google.cloud import storage, firestore
import json
import time

app = Flask(__name__)

# Configurar la conexión a google storage
storage_client = storage.Client()
bucket_name = 'vinxu-cb-bucket'
bucket = storage_client.get_bucket(bucket_name)

# Configurar la conexion a firestore
firestore_client = firestore.Client()
collection_name = 'users'
collection_ref = firestore_client.collection(collection_name)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Obtener los datos ingresados en el formulario
        # Convertir el campo 'ID' a un número entero
        id = int(request.form['id'])
        nombre = request.form['nombre']
        correo = request.form['correo']
        fecha = request.form['fecha']

        # Crear el objeto JSON con los datos del usuario
        usuario = {
            "ID": id,
            "Nombre": nombre,
            "Correo electrónico": correo,
            "Fecha de registro": fecha
        }

        # Generar un nombre único para el archivo JSON utilizando la fecha y hora actual
        # Obtener la marca de tiempo actual en segundos
        timestamp = int(time.time())
        file_name = f'datos{timestamp}.json'  # Nombre del archivo JSON

        # Guardar el objeto JSON en google storage
        blob_name = f'datos{timestamp}.json'
        blob = bucket.blob(blob_name)
        blob.upload_from_string(json.dumps(usuario))

        time.sleep(3)
        # Redireccionar a la misma página para recargar
        return redirect(url_for('index'))

    # Obtener todos los usuarios de la tabla en firestore
    query = collection_ref.stream()
    users = [doc.to_dict() for doc in query]

    return render_template('index.html', users=users)


if __name__ == '__main__':
    app.run()
