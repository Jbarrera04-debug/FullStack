from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
from dotenv import load_dotenv

# Cargar variables de entorno (opcional)
load_dotenv()

class MongoDB:
    def __init__(self):
        # Conexión a MongoDB Local o MongoDB Atlas
        self.MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        self.DATABASE_NAME = "kafeehaus_db"
        self.client = None
        self.db = None
    
    def connect(self):
        try:
            self.client = MongoClient(self.MONGO_URI)
            self.db = self.client[self.DATABASE_NAME]
            
            # Verificar conexión
            self.client.admin.command('ping')
            print("✅ Conectado a MongoDB exitosamente")
            
            # Crear índices
            self._create_indexes()
            
        except ConnectionFailure as e:
            print(f"❌ Error conectando a MongoDB: {e}")
            raise
    
    def _create_indexes(self):
        # Índices para mejor performance
        self.db.usuarios.create_index("email", unique=True)
        self.db.productos.create_index("nombre")
        self.db.pedidos.create_index("usuario_email")
        self.db.pedidos.create_index("fecha_creacion")
        
        print("✅ Índices de MongoDB creados")
    
    def get_collection(self, collection_name):
        if self.db is None:
            self.connect()
        return self.db[collection_name]
    
    def close(self):
        if self.client:
            self.client.close()
            print("🔌 Conexión a MongoDB cerrada")

# Instancia global de la base de datos
mongodb = MongoDB()