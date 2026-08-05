import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from database.models.paciente import Paciente
from extensions import db

app = create_app()
with app.app_context():
    pacientes = Paciente.query.all()
    for p in pacientes:
        print(f"ID={p.id} nombre={p.nombre} correo={p.correo} role={p.role}")
