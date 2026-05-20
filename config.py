import os
from dotenv import load_dotenv

load_dotenv()  # Carga variables de entorno desde .env (opcional en desarrollo)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave_secreta_ing_bogota_2026'
    
    # Configuración SQL con fallback a valores locales
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI',
        'mysql+pymysql://root:@localhost/gestion_medica'
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración NoSQL (MongoDB) con fallback a localhost
    MONGO_URI = os.environ.get(
        'MONGO_URI',
        'mongodb://localhost:27017/gestion_medica_nosql'
    )
    # Mail settings (SMTP)
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'localhost')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 25))
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'false').lower() in ('1', 'true', 'yes')
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'false').lower() in ('1', 'true', 'yes')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'no-reply@localhost')