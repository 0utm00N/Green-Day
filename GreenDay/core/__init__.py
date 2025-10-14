import os
import firebase_admin
from firebase_admin import credentials

# Ruta absoluta relativa al proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cred_path = os.path.join(BASE_DIR, "..", "firebase", "greendaydb-c65e3-firebase-adminsdk-fbsvc-77c97acf38.json")

# Inicializar Firebase solo si no está inicializado
if not firebase_admin._apps:
    firebase_admin.initialize_app(credentials.Certificate(cred_path))
