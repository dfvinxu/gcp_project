import json
from google.cloud import storage, firestore


def cloud_function_handler(event, context):
    '''
    Función de Cloud Functions de Google Cloud.
    El objetivo es actualizar una tabla creada en Cloud Firestore con los
    datos del archivo JSON.
    Se lanza mediante un trigger que se activa cuando se realiza un commit
    a la rama 'main' del repositorio.
    '''

    # Configurar la conexión a Cloud Firestore
    firestore_client = firestore.Client()
    collection_name = 'users'
    collection_ref = firestore_client.collection(collection_name)

    # Obtener el nombre del archivo JSON creado en Cloud Storage
    bucket = 'vinxu-cb-bucket'
    key = event['name']

    # Leer el contenido del archivo JSON desde Cloud Storage
    bucket_client = storage.Client()
    bucket = bucket_client.get_bucket(bucket)
    blob = bucket.blob(key)
    json_data = blob.download_as_text()

    # Convertir el JSON a un diccionario de Python
    data = json.loads(json_data)

    # Guardar los datos en Cloud Firestore
    collection_ref.add(data)

    return 'Datos guardados en Cloud Firestore'
