import pymongo
from flask import current_app

class MongoService:
    def __init__(self, uri=None, db_name=None):
        # Usamos la URI de configuración o una por defecto
        self.uri = uri or "mongodb://localhost:27017/"
        self.db_name = db_name or "gestion_medica_nosql"
        self.client = None
        self.db = None

    def connect(self):
        try:
            self.client = pymongo.MongoClient(self.uri)
            self.db = self.client[self.db_name]
            print(f"Conexión exitosa a MongoDB: {self.db_name}")
        except Exception as e:
            print(f"Error al conectar a MongoDB: {e}")

    def obtener_historial(self, paciente_id):
        """
        Ejemplo de cómo recuperar datos NoSQL (Historial Clínico).
        """
        if self.db is None: self.connect()
        # Buscamos en la colección 'historiales'
        return list(self.db.historiales.find({"paciente_id": paciente_id}))

    def guardar_evento(self, evento):
        """
        Guarda logs o eventos médicos.
        """
        if self.db is None: self.connect()
        return self.db.logs.insert_one(evento)