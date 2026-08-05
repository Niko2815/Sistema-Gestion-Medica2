import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from database.models.paciente import Paciente

app = create_app()
with app.app_context():
    pacientes = Paciente.query.all()
    for p in pacientes:
        print(f'{p.id} {p.nombre} {p.correo} {p.role}')
